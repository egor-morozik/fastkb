import argparse

from . import database, parser


def index_command(paths):
    total_indexed = 0
    for file_path in parser.get_all_files_by_pathes(paths):
        if file_path.is_file():
            data = parser.extract_file_data_by_path(file_path)
            if data:
                database.insert_document_to_database(**data)
                total_indexed += 1
    print(f"Index all. Processed: {total_indexed}")


def main():
    argument_parser = argparse.ArgumentParser(
        prog="fastkb",
        description="FastKB CLI tool",
    )

    subparsers = argument_parser.add_subparsers(
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
        help="Paths or files to index",
    )

    query_parser = subparsers.add_parser(
        "query",
        help="Find by database",
    )
    query_parser.add_argument(
        "text",
        help="Text for search",
    )

    arguments = argument_parser.parse_args()

    if arguments.command == "init":
        database.init_database()
    elif arguments.command == "index":
        index_command(arguments.path)
    elif arguments.command == "query":
        results = database.search_documents_in_database(arguments.text)
        if not results:
            print("Can't find.")
        else:
            print(f"Top-5 for '{arguments.text}':")
            search_lower = arguments.text.lower()

            for i, (path, content) in enumerate(results, 1):
                lines = content.splitlines()
                matching_lines = [
                    idx
                    for idx, line in enumerate(lines, start=1)
                    if search_lower in line.lower()
                ]

                if matching_lines:
                    lines_str = ", ".join(map(str, matching_lines))
                    print(f"{i}. {path} (strings: {lines_str})")
                else:
                    print(f"{i}. {path} (FTS matching, can't find strings)")
    else:
        argument_parser.print_help()


if __name__ == "__main__":
    main()
