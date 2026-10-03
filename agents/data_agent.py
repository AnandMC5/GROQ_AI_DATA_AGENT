import re

from agents.sql_agent import answer_question
from agents.profile_agent import profile_question


def classify_question(question: str) -> str:
    """
    Decide which agent should handle the user's request.

    Returns:
        SQL
        PROFILE
    """

    prompt = f"""
You are the routing agent of a Data Engineering Agent.

Your job is to decide which specialized agent should
handle the user's request.

Available agents:

1. SQL AGENT
   Use this when the user is asking questions about
   structured data stored in a database.

   Examples:
   - counts
   - averages
   - totals
   - database records
   - filtering data
   - grouping data
   - ranking records
   - comparing database values
   - database analysis

2. PROFILE AGENT
   Use this when the user wants to analyze or profile
   a data file.

   Examples:
   - CSV
   - PSV
   - Excel
   - XLSX
   - columns
   - data types
   - missing values
   - null values
   - duplicates
   - unique values
   - data quality
   - file statistics
   - profiling a dataset

Important:

- Do not assume any table names.
- Do not assume any file names.
- Do not assume any specific dataset.
- Base the decision only on the user's request.

Return ONLY one of:

SQL

PROFILE

User request:

{question}
"""

    from utils.groq_client import ask_groq

    result = ask_groq(prompt).strip().upper()

    if "PROFILE" in result:
        return "PROFILE"

    return "SQL"


def extract_file_path(question: str) -> str | None:
    """
    Try to extract a file path from the user's question.

    No specific file name is hardcoded.
    """

    # Windows paths
    windows_paths = re.findall(
        r'[A-Za-z]:\\[^"\n]+?\.(?:csv|psv|xlsx)',
        question,
        flags=re.IGNORECASE,
    )

    if windows_paths:
        return windows_paths[0].strip()

    # Quoted paths
    quoted_paths = re.findall(
        r'["\']([^"\']+\.(?:csv|psv|xlsx))["\']',
        question,
        flags=re.IGNORECASE,
    )

    if quoted_paths:
        return quoted_paths[0].strip()

    return None


def run_data_agent(question: str) -> dict:
    """
    Main Data Agent.

    User request
          ↓
    Classifier
          ↓
    SQL Agent / Profile Agent
    """

    route = classify_question(question)

    if route == "SQL":

        response = answer_question(question)

        return {
            "route": "SQL",
            "question": question,
            "response": response,
        }

    file_path = extract_file_path(question)

    if not file_path:
        return {
            "route": "PROFILE",
            "question": question,
            "response": None,
            "file_path": None,
            "message": (
                "Please provide the path of the CSV, PSV, "
                "or XLSX file that you want to profile."
            ),
        }

    response = profile_question(
        question=question,
        file_path=file_path,
    )

    return {
        "route": "PROFILE",
        "question": question,
        "response": response,
        "file_path": file_path,
    }