# FastKB

A minimalist CLI tool for indexing and searching local text files using SQLite FTS5. Fast, offline, and zero-dependency.

## Features

- **Fast Indexing**: Recursively scans directories and files.
- **Full-Text Search**: Instant ranked search (BM25) via SQLite FTS5.
- **Auto-Sync**: SQL triggers keep the search index updated automatically.
- **In-Memory Mode**: Run entirely in RAM for zero-disk-footprint operations.

## Installation

**Core (CLI + FTS5 search):**

```bash
pip install fastkb
```

**With AI/MCP support:**

```bash
pip install "fastkb[mcp]"
```

## Quick Start

### 1. Initialize

Create the database and search triggers:

```bash
fastkb init
```

### 2. Index

Scan folders or specific files:

```bash
fastkb index ./docs ./notes.txt
```

### 3. Search

Search for content (returns top 5 results by default):

```bash
fastkb query "your search term"
```

## Advanced Usage

### In-Memory Mode

Use `--memory` (`-m`) to run the database entirely in RAM. Ideal for CI/CD pipelines, automated tests, or temporary scans that shouldn't leave files on disk.

```bash
fastkb --memory index ./src
fastkb --memory query "timeout error"
```

> **Note:** The in-memory database is transient and clears when the process exits. Best used for single-session workflows or scripted runs.

## CLI Reference

### Commands

| Command | Arguments           | Description                            |
| :------ | :------------------ | :------------------------------------- |
| `init`  | -                   | Initialize database and FTS index      |
| `index` | `paths [paths ...]` | Index directories or files recursively |
| `query` | `text`              | Search the indexed knowledge base      |

### Global & Query Options

| Flag           | Scope   | Default | Description                                |
| :------------- | :------ | :------ | :----------------------------------------- |
| `-m, --memory` | Global  | `false` | Use in-memory database (non-persistent)    |
| `-l, --limit`  | `query` | `5`     | Maximum number of search results to return |

## AI Integration

FastKB supports the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) for seamless integration with Claude Desktop, Cursor, Cline, Continue, and other AI assistants.
