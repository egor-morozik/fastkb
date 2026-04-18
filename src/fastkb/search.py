from .database import find_documents


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
    for i, (path, content) in enumerate(results, 1):
        matching = extract_matching_lines(content, query)
        if matching:
            lines_str = ", ".join(map(str, matching))
            lines.append(f"{i}. {path} (lines: {lines_str})")
        else:
            lines.append(f"{i}. {path} (FTS match, exact lines not found)")

    return "\n".join(lines)


def execute_search(query, limit=5):
    """
    Run FTS5 search and print formatted results.
    """

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
