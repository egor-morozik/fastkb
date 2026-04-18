from .database import init_database
from .files import load_documents
from .search import execute_search


def handle_init(args):
    init_database()


def handle_index(args):
    count = load_documents(args.paths)
    print(f"Indexing complete. Processed: {count} file(s).")


def handle_query(args):
    execute_search(
        args.text,
        limit=args.limit,
    )
