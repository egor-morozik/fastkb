from .database import init_database
from .files import load_documents
from .search import execute_search


def handle_init(args):
    init_database()


def handle_index(args):
    load_documents(args.paths)


def handle_query(args):
    execute_search(args.text)
