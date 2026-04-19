from pathlib import Path

from .database import save_documents
from .settings import config


def iter_paths(paths):
    """
    Recursively yield file paths from given directories or files.
    """

    for path in paths:
        path = Path(path)
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from path.rglob("*")


def read_document(file_path):
    """
    Read file content and return metadata dict, or None on failure.
    """

    try:
        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
        file_statistic = file_path.stat()
        return {
            "path": str(file_path.resolve()),
            "content": content,
            "file_type": file_path.suffix.lower(),
            "file_size": file_statistic.st_size,
        }
    except Exception as exception:
        print(f"Skipping {file_path}: {exception}")
        return None


def load_documents(paths):
    """
    Walk paths, read documents, and save them in batches.
    """

    number_of_documents = 0
    batch_size = config.batch_size
    batch = []

    for file_path in iter_paths(paths):
        if not file_path.is_file():
            continue

        document = read_document(file_path)
        if document:
            batch.append(document)
            number_of_documents += 1

            if len(batch) >= batch_size:
                save_documents(batch)
                batch.clear()
    if batch:
        save_documents(batch)

    print(f"Indexing complete. Processed: {number_of_documents} file(s).")
