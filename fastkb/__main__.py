import sys

import sqlite3

import argparse

from pathlib import Path


def init_db():
    """
    Create database fastkb.db and documents table.
    """

    try:
        connection = sqlite3.connect("fastkb.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE,
                content TEXT,
                file_type TEXT,
                file_size INTEGER
            )
            """
        )

        cursor.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts 
            USING fts5(path, content, content='documents', content_rowid='id')
            """
        )

        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
            INSERT INTO documents_fts(rowid, path, content) VALUES (new.id, new.path, new.content);
            END
            """
        )

        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
            INSERT INTO documents_fts(documents_fts, rowid, path, content) 
            VALUES('delete', old.id, old.path, old.content);
            END
            """
        )

        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
            INSERT INTO documents_fts(documents_fts, rowid, path, content) 
            VALUES('delete', old.id, old.path, old.content);
            INSERT INTO documents_fts(rowid, path, content) 
            VALUES(new.id, new.path, new.content);
            END
            """
        )

        connection.commit()
        connection.close()
        print("Database fastkb.db init, table 'documents' created.")

    except Exception as e:
        print(f"Init database error: {e}")
        sys.exit(1)


def save_to_db(cursor, file_path):
    """
    Read file and add it to database.
    """

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        stats = file_path.stat()
        cursor.execute(
            """
            INSERT OR REPLACE INTO documents 
            (path, content, file_type, file_size)
            VALUES (?, ?, ?, ?)
            """,
            (str(file_path.absolute()), content, file_path.suffix, stats.st_size),
        )
        return True
    except Exception as e:
        print(f"Skip file {file_path}: {e}")
        return False


def index_paths(paths):
    """
    Process data to index.
    """

    connection = sqlite3.connect("fastkb.db")
    cursor = connection.cursor()
    total_indexed = 0

    for p in paths:
        path_obj = Path(p)

        targets = [path_obj] if path_obj.is_file() else path_obj.rglob("*")

        for file_path in targets:
            if file_path.is_file():
                if save_to_db(cursor, file_path):
                    total_indexed += 1

    connection.commit()
    connection.close()
    print(f"Index all. Processed: {total_indexed}")


def query_db(search_text):
    """
    Find top-5 files by query.
    """

    connection = sqlite3.connect("fastkb.db")
    cursor = connection.cursor()

    query = """
        SELECT path FROM documents_fts 
        WHERE documents_fts MATCH ? 
        ORDER BY rank 
        LIMIT 5
    """

    cursor.execute(
        query,
        (search_text,),
    )
    results = cursor.fetchall()

    if not results:
        print("Can't find.")
    else:
        print(f"Top-5 for '{search_text}':")
        for i, (path,) in enumerate(results, 1):
            print(f"{i}. {path}")

    connection.close()


def main():
    parser = argparse.ArgumentParser(
        prog="fastkb",
        description="FastKB CLI tool",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="All commands",
    )
    subparsers.add_parser(
        "init",
        help="Init database",
    )

    index_parser = subparsers.add_parser("index")
    index_parser.add_argument(
        "path",
        nargs="+",
        help="Pathes or files to index",
    )

    query_parser = subparsers.add_parser(
        "query",
        help="Find by database",
    )
    query_parser.add_argument(
        "text",
        help="Text for search",
    )

    args = parser.parse_args()

    if args.command == "init":
        init_db()
    elif args.command == "index":
        index_paths(args.path)
    elif args.command == "query":
        query_db(args.text)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
