import sqlite3

from contextlib import contextmanager

from .settings import config


@contextmanager
def get_connection():
    """
    Yield a SQLite connection with WAL mode enabled.
    """

    connection = sqlite3.connect(config.db_path)

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        if not config.memory_mode:
            connection.close()


def init_database():
    """
    Create documents table, FTS5 virtual table, and sync triggers.
    """

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts
            USING fts5(path, content, content='documents', content_rowid='id', tokenize="unicode61")
            """
        )
        connection.execute(
            """
            CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
                INSERT INTO documents_fts(rowid, path, content) VALUES (new.id, new.path, new.content);
            END
            """
        )
        connection.execute(
            """
            CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
                INSERT INTO documents_fts(documents_fts, rowid, path, content)
                VALUES('delete', old.id, old.path, old.content);
            END
            """
        )
        connection.execute(
            """
            CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
                INSERT INTO documents_fts(documents_fts, rowid, path, content)
                VALUES('delete', old.id, old.path, old.content);
                INSERT INTO documents_fts(rowid, path, content)
                VALUES(new.id, new.path, new.content);
            END
            """
        )
    print(f"Database '{config.db_path}' initialized successfully.")


def save_documents(documents):
    """
    Insert or update multiple documents in a single transaction.
    """

    if not documents:
        return
    query = """
            INSERT INTO documents (path, content, file_type, file_size)
            VALUES (:path, :content, :file_type, :file_size)
            ON CONFLICT(path) DO UPDATE SET
                content = excluded.content,
                file_type = excluded.file_type,
                file_size = excluded.file_size
            """
    with get_connection() as connection:
        connection.executemany(query, documents)


def find_documents(query, limit):
    """
    Execute FTS5 search and return (path, content) tuples.
    """

    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT d.path, d.content
            FROM documents_fts f
            JOIN documents d ON f.rowid = d.id
            WHERE documents_fts MATCH ?
            ORDER BY f.rank
            LIMIT ?
            """,
            (
                query,
                limit,
            ),
        )
        return cursor.fetchall()
