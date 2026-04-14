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

### 3. Query

Search for content (returns top 5 results):

```bash
python fastkb query "your search term"
```

### Commands

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `init` | - | Setup fastkb.db and FTS5 tables. |
| `index` | `path [path ...]` | Index folders or files recursively. |
| `query` | `text` | Search ranked results by content. |
