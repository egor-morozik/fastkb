# FastKB

A minimalist CLI tool for indexing and searching local text files using SQLite FTS5.

## Features

**Fast Indexing**: Recursively scans directories and files.
**Full-Text Search**: Instant ranked search (BM25) via SQLite FTS5.
**Auto-Sync**: SQL triggers keep the search index updated automatically.

## Quick Start

### 1. Initialize

Create the database and search triggers:

```bash
python fastkb init
```

### 2. Index

Scan folders or specific files:

```bash
python fastkb index ./docs ./notes.txt
```

### 3. Search

Search for content (returns top 5 results by default):

```bash
python fastkb query "your search term"
```

### Commands

| Command | Arguments           | Description                            |
| :------ | :------------------ | :------------------------------------- |
| `init`  | -                   | Initialize database and FTS index      |
| `index` | `paths [paths ...]` | Index directories or files recursively |
| `query` | `text`              | Search the indexed knowledge base      |

### Query Options

| Option        | Default | Description                                |
| :------------ | :------ | :----------------------------------------- |
| `-l, --limit` | `5`     | Maximum number of search results to return |