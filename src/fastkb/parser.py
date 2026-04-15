from pathlib import Path


def extract_file_data_by_path(file_path):
    """
    Read file and return data for database.
    """

    try:
        file_content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
        file_statistics = file_path.stat()
        return {
            "path": str(file_path.absolute()),
            "content": file_content,
            "file_type": file_path.suffix,
            "file_size": file_statistics.st_size,
        }
    except Exception as exception_instance:
        print(f"Skip file {file_path}: {exception_instance}")
        return None


def get_all_files_by_pathes(target_pathes):
    """
    Generator that return all files.
    """

    for current_path in target_pathes:
        path_object = Path(current_path)
        if path_object.is_file():
            yield path_object
        else:
            yield from path_object.rglob("*")
            