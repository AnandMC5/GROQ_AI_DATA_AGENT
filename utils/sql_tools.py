import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA")


def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def get_database_schema():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Get tables from the configured schema
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s
              AND table_type = 'BASE TABLE'
            ORDER BY table_name;
            """,
            (POSTGRES_SCHEMA,),
        )

        tables = [row[0] for row in cursor.fetchall()]

        database_schema = {}

        for table_name in tables:

            # Get columns and data types
            cursor.execute(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = %s
                  AND table_name = %s
                ORDER BY ordinal_position;
                """,
                (POSTGRES_SCHEMA, table_name),
            )

            columns = [
                {
                    "column_name": row[0],
                    "data_type": row[1]
                }
                for row in cursor.fetchall()
            ]

            # Get only 5 sample rows
            cursor.execute(
                f'''
                SELECT *
                FROM "{POSTGRES_SCHEMA}"."{table_name}"
                LIMIT 5;
                '''
            )

            rows = cursor.fetchall()

            column_names = [
                description[0]
                for description in cursor.description
            ]

            sample_rows = [
                dict(zip(column_names, row))
                for row in rows
            ]

            database_schema[table_name] = {
                "columns": columns,
                "sample_rows": sample_rows,
            }

        cursor.close()

        return database_schema

    finally:
        connection.close()


def is_safe_sql(sql: str) -> bool:
    """
    Allow only SELECT or WITH queries.
    Block database modification commands.
    """

    sql = sql.strip().lower()

    if not sql:
        return False

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "replace",
        "grant",
        "revoke",
    ]

    for keyword in forbidden_keywords:
        if keyword in sql:
            return False

    return sql.startswith("select") or sql.startswith("with")


def execute_query(sql: str, max_rows: int = 10) -> list:
    """
    Execute a read-only SQL query.

    Only the first max_rows rows are returned.
    This prevents large query results from being
    sent to Groq.
    """

    if not is_safe_sql(sql):
        raise ValueError(
            "Unsafe SQL query. Only SELECT and WITH queries are allowed."
        )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(sql)

        columns = [
            description[0]
            for description in cursor.description
        ]

        # IMPORTANT:
        # Do not fetch the complete result.
        rows = cursor.fetchmany(max_rows)

        result = [
            dict(zip(columns, row))
            for row in rows
        ]

        cursor.close()

        return result

    finally:
        connection.close()