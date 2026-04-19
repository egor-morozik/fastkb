from .database import find_documents
from .settings import config


def extract_matching_lines(content, query):
    """
    Return 1-based line numbers containing the query (case-insensitive).
    """

    query_lower = query.lower()
    return [
        index
        for index, line in enumerate(
            content.splitlines(),
            start=1,
        )
        if query_lower in line.lower()
    ]


def format_results(results, query):
    """
    Format search results for CLI output.
    """

    if not results:
        return "No results found."

    lines = [f"Top-{len(results)} for '{query}':\n"]
    for index, (path, content) in enumerate(results, 1):
        matching = extract_matching_lines(content, query)
        if matching:
            lines_str = ", ".join(map(str, matching))
            lines.append(f"{index}. {path} (lines: {lines_str})")
        else:
            lines.append(f"{index}. {path} (FTS match, exact lines not found)")

    return "\n".join(lines)


def execute_search(query):
    """
    Run FTS5 search and print formatted results.
    """

    limit = config.search_limit
    results = find_documents(
        query,
        limit,
    )

    print(
        format_results(
            results,
            query,
        )
    )
