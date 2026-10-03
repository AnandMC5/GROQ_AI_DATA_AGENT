import os

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".psv",
    ".xlsx",
}


def _to_python_value(value):
    """
    Convert Pandas/NumPy values into normal Python values.
    """

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def _detect_date_column(series):
    """
    Detect whether a column appears to contain dates.
    """

    if not (
        pd.api.types.is_object_dtype(series)
        or pd.api.types.is_string_dtype(series)
    ):
        return False

    non_null = series.dropna()

    if non_null.empty:
        return False

    converted = pd.to_datetime(
        non_null,
        errors="coerce"
    )

    valid_ratio = converted.notna().mean()

    return valid_ratio >= 0.80


def _is_numeric(series):
    """
    Check whether a column contains numeric data.
    """

    return pd.api.types.is_numeric_dtype(series)


def _read_file_in_chunks(file_path, chunk_size):
    """
    Read CSV/PSV files in chunks.

    Excel files are read sheet-by-sheet.
    """

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".csv":

        return pd.read_csv(
            file_path,
            chunksize=chunk_size
        )

    if extension == ".psv":

        return pd.read_csv(
            file_path,
            sep="|",
            chunksize=chunk_size
        )

    if extension == ".xlsx":

        # Excel does not support Pandas chunksize
        # in the same way as CSV.
        #
        # Read each sheet separately.

        excel_file = pd.ExcelFile(file_path)

        chunks = []

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

                chunks.append(
                    dataframe.iloc[
                        start:start + chunk_size
                    ]
                )

        return chunks

    raise ValueError(
        f"Unsupported file type: {extension}. "
        f"Supported types: {SUPPORTED_EXTENSIONS}"
    )


def profile_large_file(
    file_path: str,
    chunk_size: int = 100_000
) -> dict:
    """
    Profile large CSV, PSV, or XLSX files.

    The profiler is schema-agnostic.
    """

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types: "
            f"{', '.join(sorted(SUPPORTED_EXTENSIONS))}"
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

    sample_values = {}
    date_columns = {}

    duplicate_count = 0

    seen_rows = set()

    chunks = _read_file_in_chunks(
        file_path,
        chunk_size
    )

    for chunk in chunks:

        if column_names is None:

            column_names = list(
                chunk.columns
            )

            for column in column_names:

                null_counts[column] = 0
                empty_string_counts[column] = 0

                unique_values[column] = set()

                sample_values[column] = []

                date_columns[column] = False

        total_rows += len(chunk)

        # --------------------------------------------------
        # COLUMN PROCESSING
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
                pd.api.types.is_object_dtype(series)
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

            if len(
                unique_values[column]
            ) < 100_000:

                values = (
                    series
                    .dropna()
                    .unique()
                    .tolist()
                )

                remaining = (
                    100_000
                    - len(
                        unique_values[column]
                    )
                )

                unique_values[column].update(
                    values[:remaining]
                )

            # --------------------------------------------------
            # SAMPLE VALUES
            # --------------------------------------------------

            if len(
                sample_values[column]
            ) < 5:

                values = (
                    series
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                remaining = (
                    5
                    - len(
                        sample_values[column]
                    )
                )

                sample_values[column].extend(
                    values[:remaining]
                )

            # --------------------------------------------------
            # NUMERIC STATISTICS
            # --------------------------------------------------

            if _is_numeric(series):

                numeric_series = (
                    series.dropna()
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

                    current_min = (
                        _to_python_value(
                            current_min
                        )
                    )

                    current_max = (
                        _to_python_value(
                            current_max
                        )
                    )

                    current_sum = (
                        _to_python_value(
                            current_sum
                        )
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

                    sum_values[column] = (
                        sum_values.get(
                            column,
                            0
                        )
                        + current_sum
                    )

                    numeric_counts[column] = (
                        numeric_counts.get(
                            column,
                            0
                        )
                        + current_count
                    )

            # --------------------------------------------------
            # DATE DETECTION
            # --------------------------------------------------

            if not date_columns[column]:

                if _detect_date_column(
                    series
                ):

                    date_columns[column] = True

        # --------------------------------------------------
        # DUPLICATE DETECTION
        # --------------------------------------------------

        row_hashes = (
            pd.util.hash_pandas_object(
                chunk,
                index=False
            )
        )

        for row_hash in row_hashes:

            row_hash = int(row_hash)

            if row_hash in seen_rows:

                duplicate_count += 1

            else:

                seen_rows.add(row_hash)

        del chunk

    # ------------------------------------------------------
    # COLUMN PROFILE
    # ------------------------------------------------------

    column_profile = {}

    for column in column_names:

        null_count = null_counts[column]

        non_null_count = (
            total_rows
            - null_count
        )

        null_percentage = (
            (
                null_count
                / total_rows
            )
            * 100
            if total_rows > 0
            else 0
        )

        unique_count = len(
            unique_values[column]
        )

        unique_percentage = (
            (
                unique_count
                / non_null_count
            )
            * 100
            if non_null_count > 0
            else 0
        )

        profile = {
            "data_type":
                data_types.get(column),

            "null_count":
                null_count,

            "null_percentage":
                round(
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

            "possible_date_column":
                date_columns[column],

            "sample_values":
                sample_values[column],
        }

        # Numeric statistics
        if column in min_values:

            profile["min"] = (
                min_values[column]
            )

            profile["max"] = (
                max_values[column]
            )

            count = numeric_counts[column]

            if count > 0:

                profile["mean"] = round(
                    sum_values[column]
                    / count,
                    2
                )

        column_profile[column] = profile

    # ------------------------------------------------------
    # QUALITY ISSUES
    # ------------------------------------------------------

    quality_issues = []

    for column, profile in (
        column_profile.items()
    ):

        if profile["null_count"] > 0:

            quality_issues.append(
                {
                    "type":
                        "missing_values",

                    "column":
                        column,

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
                    "type":
                        "empty_strings",

                    "column":
                        column,

                    "count":
                        profile[
                            "empty_string_count"
                        ],
                }
            )

        if (
            profile["unique_count"] == 1
            and profile["null_count"]
            < total_rows
        ):

            quality_issues.append(
                {
                    "type":
                        "constant_column",

                    "column":
                        column,
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

    # ------------------------------------------------------
    # FINAL RESULT
    # ------------------------------------------------------

    return {
        "file":
            os.path.basename(
                file_path
            ),

        "file_type":
            extension,

        "file_size_bytes":
            os.path.getsize(
                file_path
            ),

        "processing_mode":
            "large_file_chunked",

        "total_rows":
            total_rows,

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