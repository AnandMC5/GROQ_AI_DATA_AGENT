import json
from decimal import Decimal

from utils.groq_client import ask_groq
from utils.sql_tools import (
    get_database_schema,
    execute_query,
)


def make_json_safe(value):
    """
    Convert PostgreSQL/Python values into JSON-safe values.
    """

    if isinstance(value, dict):
        return {
            key: make_json_safe(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, Decimal):
        return float(value)

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value


def build_schema_context():
    """
    Get database schema and convert it into
    a JSON string that can be sent to Groq.
    """

    database_schema = get_database_schema()

    safe_schema = make_json_safe(database_schema)

    return json.dumps(
        safe_schema,
        indent=2
    )


def generate_sql(question: str) -> str:
    """
    Convert a natural-language question into
    a read-only PostgreSQL SQL query.
    """

    schema_context = build_schema_context()

    prompt = f"""
You are a PostgreSQL SQL generation agent.

Your task is to convert the user's natural-language
question into ONE read-only PostgreSQL SQL query.

Database schema:

{schema_context}

Rules:

1. Use only tables and columns that exist in the schema.

2. The tables are inside the PostgreSQL schema:
   public

3. Always use the full table name:
   public.table_name

4. Generate only SELECT or WITH queries.

5. Never generate:
   INSERT
   UPDATE
   DELETE
   DROP
   ALTER
   TRUNCATE
   CREATE
   GRANT
   REVOKE

6. Never modify database data.

7. Do not return explanations.

8. Return ONLY the SQL query.

9. For questions asking for:
   - lists
   - rankings
   - top records
   - highest
   - lowest
   - most
   - least
   - users with the most rides
   - users with the highest values
   - similar questions

   return at most 10 rows using:

   LIMIT 10

10. If aggregation is required, use GROUP BY
    and return only the required result.

11. If the question asks for a count, sum, average,
    minimum, maximum, or other aggregate value,
    return the aggregate result instead of raw rows.

12. Do not use tables outside the provided schema.

User question:

{question}
"""

    sql = ask_groq(prompt)

    return sql.strip()


def answer_question(question: str) -> dict:
    """
    Complete SQL Agent workflow:

    Natural language question
            ↓
    Generate SQL using Groq
            ↓
    Execute SQL
            ↓
    Limit result rows
            ↓
    Generate natural-language answer using Groq
    """

    # -------------------------------------------------
    # Step 1: Generate SQL
    # -------------------------------------------------

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print("-" * 60)
    print(sql)

    # -------------------------------------------------
    # Step 2: Execute SQL
    # -------------------------------------------------

    result = execute_query(
        sql,
        max_rows=10
    )

    # -------------------------------------------------
    # Step 3: Convert PostgreSQL values to JSON-safe
    # -------------------------------------------------

    result = make_json_safe(result)

    result_json = json.dumps(
        result,
        indent=2
    )

    # -------------------------------------------------
    # Step 4: Ask Groq to explain the result
    # -------------------------------------------------

    prompt = f"""
You are a data analyst.

Answer the user's question using ONLY the SQL result
provided below.

Do not invent information.

User question:

{question}

SQL result:

{result_json}

Give a clear and concise natural-language answer.

If the result contains multiple rows,
summarize the important information clearly.

Do not generate SQL.
Do not add information that is not present
in the SQL result.
"""

    answer = ask_groq(prompt)

    return {
        "sql": sql,
        "result": result,
        "answer": answer,
    }