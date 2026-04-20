import argparse


def build_parser():
    parser = argparse.ArgumentParser(
        prog="fastkb",
        description="Fast local knowledge base with FTS5 search.",
    )

    parser.add_argument(
        "--memory",
        "-m",
        action="store_true",
        help="Use in-memory database (non-persistent)",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )
    subparsers.add_parser(
        "init",
        help="Initialize database and FTS index.",
    )

    index_parser = subparsers.add_parser(
        "index",
        help="Index files into the database.",
    )
    index_parser.add_argument(
        "paths",
        nargs="+",
        help="Directories or files to index.",
    )

    query_parser = subparsers.add_parser(
        "query",
        help="Search the indexed knowledge base.",
    )
    query_parser.add_argument(
        "text",
        help="Search query (FTS5 syntax).",
    )
    query_parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=5,
        help="Max results (default: 5).",
    )

    return parser
