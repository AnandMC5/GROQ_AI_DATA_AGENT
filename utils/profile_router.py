import os

from utils.data_tools import profile_file as profile_small_file
from utils.large_data_tools import profile_large_file


SMALL_FILE_LIMIT = 500 * 1024  # 500 KB


def profile_file(file_path: str) -> dict:
    """
    Automatically select the small-file or large-file
    profiler based on file size.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    file_size = os.path.getsize(file_path)

    print(f"File: {file_path}")
    print(f"File size: {file_size} bytes")

    # --------------------------------------------------
    # SMALL FILE
    # --------------------------------------------------

    if file_size <= SMALL_FILE_LIMIT:

        print("Processing mode: SMALL FILE")

        result = profile_small_file(
            file_path
        )

        result["processing_mode"] = "small_file"

        return result

    # --------------------------------------------------
    # LARGE FILE
    # --------------------------------------------------

    print("Processing mode: LARGE FILE")

    result = profile_large_file(
        file_path
    )

    result["processing_mode"] = "large_file"

    return result