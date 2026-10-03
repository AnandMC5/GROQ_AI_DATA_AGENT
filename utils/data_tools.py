import os

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".psv",
    ".xlsx",
}


def _read_file_in_chunks(
    file_path: str,
    chunk_size: int
):
    """
    Read CSV, PSV, or XLSX files in chunks.

    CSV and PSV are read directly in chunks.

    XLSX is loaded as a DataFrame first and then
    divided into smaller chunks. Since this profiler
    is used for small files, this is acceptable.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":

        for chunk in pd.read_csv(
            file_path,
            chunksize=chunk_size
        ):
            yield chunk

    elif extension == ".psv":

        for chunk in pd.read_csv(
            file_path,
            sep="|",
            chunksize=chunk_size
        ):
            yield chunk

    elif extension == ".xlsx":

        excel_file = pd.ExcelFile(file_path)

        for sheet_name in excel_file.sheet_names:

            dataframe = pd.read_excel(
                file_path,
                sheet_name=sheet_name
            )

            for start in range(
                0,
                len(dataframe),
                chunk_size
            ):

                yield dataframe.iloc[
                    start:start + chunk_size
                ].copy()

    else:

        raise ValueError(
            f"Unsupported file format: {extension}. "
            f"Supported formats: {SUPPORTED_EXTENSIONS}"
        )


def _to_python_value(value):
    """
    Convert Pandas/NumPy values into normal
    Python values so the final result is JSON-safe.
    """

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        try:
            return value.item()
        except (ValueError, TypeError):
            pass

    return value


def profile_file(
    file_path: str,
    chunk_size: int = 100_000
) -> dict:
    """
    Profile CSV, PSV, or XLSX files.

    The profiler is schema-agnostic and does not
    assume any specific column names.

    It collects generic data-quality and profiling
    information that can later be passed to GROQ.
    """

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(
            f"Unsupported file format: {extension}. "
            f"Supported formats: {SUPPORTED_EXTENSIONS}"
        )

    total_rows = 0

    column_names = None

    data_types = {}

    null_counts = {}

    empty_string_counts = {}

    unique_values = {}

    min_values = {}

    max_values = {}

    sum_values = {}

    numeric_counts = {}

    duplicate_count = 0

    seen_rows = set()

    sample_values = {}

    # --------------------------------------------------
    # READ FILE
    # --------------------------------------------------

    for chunk in _read_file_in_chunks(
        file_path,
        chunk_size
    ):

        # --------------------------------------------------
        # BASIC INFORMATION
        # --------------------------------------------------

        if column_names is None:

            column_names = list(
                chunk.columns
            )

            for column in column_names:

                null_counts[column] = 0

                empty_string_counts[column] = 0

                unique_values[column] = set()

                sample_values[column] = []

        total_rows += len(chunk)

        # --------------------------------------------------
        # COLUMN ANALYSIS
        # --------------------------------------------------

        for column in chunk.columns:

            series = chunk[column]

            # Data type
            data_types[column] = str(
                series.dtype
            )

            # Null values
            null_counts[column] += int(
                series.isna().sum()
            )

            # Empty strings
            if (
                series.dtype == "object"
                or pd.api.types.is_string_dtype(series)
            ):

                empty_string_counts[column] += int(
                    series
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .eq("")
                    .sum()
                )

            # --------------------------------------------------
            # UNIQUE VALUES
            # --------------------------------------------------

            values = (
                series
                .dropna()
                .unique()
                .tolist()
            )

            for value in values:

                value = _to_python_value(
                    value
                )

                if value is not None:

                    unique_values[column].add(
                        value
                    )

            # --------------------------------------------------
            # SAMPLE VALUES
            # --------------------------------------------------

            existing_samples = set(
                sample_values[column]
            )

            if len(
                sample_values[column]
            ) < 5:

                values = (
                    series
                    .dropna()
                    .astype(str)
                    .tolist()
                )

                for value in values:

                    if value not in existing_samples:

                        sample_values[column].append(
                            value
                        )

                        existing_samples.add(
                            value
                        )

                    if len(
                        sample_values[column]
                    ) >= 5:

                        break

            # --------------------------------------------------
            # NUMERIC STATISTICS
            # --------------------------------------------------

            if pd.api.types.is_numeric_dtype(
                series
            ):

                numeric_series = (
                    series
                    .dropna()
                )

                if not numeric_series.empty:

                    current_min = (
                        numeric_series.min()
                    )

                    current_max = (
                        numeric_series.max()
                    )

                    current_sum = (
                        numeric_series.sum()
                    )

                    current_count = len(
                        numeric_series
                    )

                    current_min = _to_python_value(
                        current_min
                    )

                    current_max = _to_python_value(
                        current_max
                    )

                    current_sum = _to_python_value(
                        current_sum
                    )

                    if column not in min_values:

                        min_values[column] = (
                            current_min
                        )

                    else:

                        min_values[column] = min(
                            min_values[column],
                            current_min
                        )

                    if column not in max_values:

                        max_values[column] = (
                            current_max
                        )

                    else:

                        max_values[column] = max(
                            max_values[column],
                            current_max
                        )

                    if column not in sum_values:

                        sum_values[column] = (
                            current_sum
                        )

                    else:

                        sum_values[column] += (
                            current_sum
                        )

                    if column not in numeric_counts:

                        numeric_counts[column] = (
                            current_count
                        )

                    else:

                        numeric_counts[column] += (
                            current_count
                        )

        # --------------------------------------------------
        # DUPLICATE ROW DETECTION
        # --------------------------------------------------

        row_hashes = pd.util.hash_pandas_object(
            chunk,
            index=False
        )

        for row_hash in row_hashes:

            row_hash = int(row_hash)

            if row_hash in seen_rows:

                duplicate_count += 1

            else:

                seen_rows.add(
                    row_hash
                )

    # --------------------------------------------------
    # EMPTY FILE CHECK
    # --------------------------------------------------

    if column_names is None:

        return {
            "file": file_path,
            "file_type": extension,
            "total_rows": 0,
            "total_columns": 0,
            "columns": [],
            "column_profile": {},
            "duplicate_rows": 0,
            "quality_issues": [],
            "chunk_size": chunk_size,
        }

    # --------------------------------------------------
    # BUILD COLUMN PROFILE
    # --------------------------------------------------

    column_profile = {}

    for column in column_names:

        null_count = null_counts[column]

        null_percentage = (
            (null_count / total_rows) * 100
            if total_rows > 0
            else 0
        )

        unique_count = len(
            unique_values[column]
        )

        unique_percentage = (
            (unique_count / total_rows) * 100
            if total_rows > 0
            else 0
        )

        is_constant = (
            unique_count <= 1
            and total_rows > 0
        )

        profile = {

            "data_type": data_types.get(
                column
            ),

            "null_count": null_count,

            "null_percentage": round(
                null_percentage,
                2
            ),

            "empty_string_count":
                empty_string_counts[column],

            "unique_count":
                unique_count,

            "unique_percentage":
                round(
                    unique_percentage,
                    2
                ),

            "is_constant":
                is_constant,

            "sample_values":
                sample_values[column],
        }

        # --------------------------------------------------
        # NUMERIC STATISTICS
        # --------------------------------------------------

        if column in min_values:

            profile["min"] = min_values[
                column
            ]

            profile["max"] = max_values[
                column
            ]

            numeric_count = numeric_counts[
                column
            ]

            if numeric_count > 0:

                profile["mean"] = round(
                    sum_values[column]
                    / numeric_count,
                    2
                )

        column_profile[column] = profile

    # --------------------------------------------------
    # GENERIC QUALITY ISSUES
    # --------------------------------------------------

    quality_issues = []

    for column, profile in column_profile.items():

        if profile["null_count"] > 0:

            quality_issues.append(
                {
                    "type": "missing_values",
                    "column": column,
                    "count":
                        profile["null_count"],
                    "percentage":
                        profile[
                            "null_percentage"
                        ],
                }
            )

        if profile[
            "empty_string_count"
        ] > 0:

            quality_issues.append(
                {
                    "type": "empty_strings",
                    "column": column,
                    "count":
                        profile[
                            "empty_string_count"
                        ],
                }
            )

        if profile["is_constant"]:

            quality_issues.append(
                {
                    "type":
                        "constant_column",
                    "column":
                        column,
                    "unique_count":
                        profile[
                            "unique_count"
                        ],
                }
            )

    if duplicate_count > 0:

        quality_issues.append(
            {
                "type":
                    "duplicate_rows",
                "count":
                    duplicate_count,
            }
        )

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    return {

        "file": file_path,

        "file_type": extension,

        "total_rows": total_rows,

        "total_columns":
            len(column_names),

        "columns":
            column_names,

        "column_profile":
            column_profile,

        "duplicate_rows":
            duplicate_count,

        "quality_issues":
            quality_issues,

        "chunk_size":
            chunk_size,
    }