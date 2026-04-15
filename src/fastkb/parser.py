from pathlib import Path


def extract_file_data_by_path(file_path):
    """
    Read file and return data for database.
    """

    try:
        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
        stats = file_path.stat()
        return {
            "path": str(file_path.absolute()),
            "content": content,
            "file_type": file_path.suffix,
            "file_size": stats.st_size,
        }
    except Exception as expection:
        print(f"Skip file {file_path}: {expection}")
        return None


def get_all_files_by_pathes(paths):
    """
    Generator that return all files.
    """

    for path in paths:
        path_object = Path(path)
        if path_object.is_file():
            yield path_object
        else:
            yield from path_object.rglob("*")
