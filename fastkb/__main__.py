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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE,
                content TEXT,
                file_type TEXT,
                file_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        connection.close()
        print("Database fastkb.db init, table 'documents' created.")
    except Exception as e:
        print(f"Init database error: {e}")
        sys.exit(1)


def index_path(root_path):
    """
    Add documents to database.
    """

    connection = sqlite3.connect("fastkb.db")
    cursor = connection.cursor()

    indexed_count = 0
    root = Path(root_path)

    for file_path in root.rglob("*"):
        if file_path.is_file():
            try:
                content = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                stats = file_path.stat()

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO documents 
                    (path, content, file_type, file_size)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        str(file_path.absolute()),
                        content,
                        file_path.suffix,
                        stats.st_size,
                    ),
                )
                indexed_count += 1
            except Exception as e:
                print(f"Skip file {file_path}: {e}")

    connection.commit()
    connection.close()
    print(f"Index all. Proccesed: {indexed_count}")


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
        help="Path or file to index",
    )

    args = parser.parse_args()

    if args.command == "init":
        init_db()
    elif args.command == "index":
        index_path(args.path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
