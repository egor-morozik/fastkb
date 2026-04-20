import os

from mcp.server.fastmcp import FastMCP
from .database import find_documents
from .settings import config


mcp = FastMCP("FastKB")


@mcp.tool()
def search(query, limit=5):
    """
    Search local knowledge base.
    Returns file paths, matching line numbers, and text preview.
    """

    config.configure(
        memory=False,
        limit=limit,
    )

    if db_path := os.getenv("FASTKB_DB_PATH"):
        config.db_path = db_path

    raw_results = find_documents(query, limit)
    results = []
    query_lower = query.lower()

    for path, content in raw_results:
        matching_lines = [
            index
            for index, line in enumerate(
                content.splitlines(),
                1,
            )
            if query_lower in line.lower()
        ]
        results.append(
            {
                "path": path,
                "matching_lines": matching_lines,
                "preview": content[:500].replace("\n", " "),
            }
        )

    return results


def run():
    """
    Run via stdio.
    """

    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
