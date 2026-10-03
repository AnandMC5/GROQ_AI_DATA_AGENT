import json

from utils.profile_router import profile_file
from utils.groq_client import ask_groq


def profile_question(
    question: str,
    file_path: str,
) -> dict:
    """
    Profile a data file and generate a natural-language
    interpretation of the profiling results.
    """

    profile_result = profile_file(file_path)

    profile_json = json.dumps(
        profile_result,
        indent=2,
        default=str,
    )

    prompt = f"""
You are a senior data engineer analyzing a dataset profile.

User request:

{question}

Dataset profiling information:

{profile_json}

Analyze ONLY the information provided.

Provide a concise and useful explanation covering,
where applicable:

- dataset size
- columns
- data types
- missing values
- duplicate records
- unique values
- constant columns
- numeric statistics
- data quality issues
- important observations

Do not invent information.

Do not return JSON.

Return a clear human-readable response.
"""

    analysis = ask_groq(prompt)

    return {
        "file_path": file_path,
        "profile": profile_result,
        "analysis": analysis,
    }