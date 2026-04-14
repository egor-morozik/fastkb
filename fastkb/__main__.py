import sqlite3

import argparse

import sys


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
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        connection.close()
        print("Database fastkb.db init, table 'documents' created.")
    except Exception as e:
        print(f"Init database error: {e}")
        sys.exit(1)


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

    args = parser.parse_args()

    if args.command == "init":
        init_db()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
