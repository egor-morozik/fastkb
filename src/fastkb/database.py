import sqlite3

import sys


DATABASE_NAME = "fastkb.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def init_database():
    """
    Create database DATABASE_NAME and documents table.
    """

    try:
        with get_connection() as connection:
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
            USING fts5(path, content, content='documents', content_rowid='id', tokenize="unicode61")
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
        print(f"Database {DATABASE_NAME} initialized.")
    except Exception as expection:
        print(f"Init database error: {expection}")
        sys.exit(1)


def insert_document_to_database(path, content, file_type, file_size):
    """
    Insert file data to database.
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO documents 
            (path, content, file_type, file_size) 
            VALUES (?, ?, ?, ?)
            """,
            (path, content, file_type, file_size),
        )
        connection.commit()


def search_documents_in_database(search_text, limit=5):
    """
    Search files at database by text (by file name and content).
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT path 
            FROM documents_fts 
            WHERE documents_fts MATCH ? 
            ORDER BY rank 
            LIMIT ?
            """,
            (search_text, limit),
        )
        return cursor.fetchall()
