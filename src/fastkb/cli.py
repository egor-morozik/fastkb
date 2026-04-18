import sys
import argparse

from .database import init_database
from .files import load_documents
from .search import execute_search


def parse_args():
    parser = argparse.ArgumentParser(
        prog="fastkb",
        description="Fast local knowledge base with FTS5 search.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )
    subparsers.add_parser(
        "init",
        help="Initialize database and FTS index.",
    )

    index_cmd = subparsers.add_parser(
        "index",
        help="Index files into the database.",
    )
    index_cmd.add_argument(
        "paths",
        nargs="+",
        help="Directories or files to index.",
    )

    query_cmd = subparsers.add_parser(
        "query", help="Search the indexed knowledge base."
    )
    query_cmd.add_argument(
        "text",
        help="Search query (FTS5 syntax).",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        if args.command == "init":
            init_database()
        elif args.command == "index":
            count = load_documents(args.paths)
            print(f"Indexing complete. Processed: {count} file(s).")
        elif args.command == "query":
            execute_search(
                args.text,
                limit=args.limit,
            )
    except Exception as expection:
        print(f"\nError: {expection}")
        sys.exit(1)
