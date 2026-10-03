import os
import re
from datetime import datetime

from utils.groq_client import ask_groq


REPORT_FOLDER = "C:/PROJECTS/GROK_DATA_AGENT/reports"


def create_report_filename(question: str) -> str:
    """
    Create a readable report filename from the question.
    """

    words = re.findall(
        r"[a-zA-Z0-9]+",
        question.lower(),
    )

    name = "_".join(words[:8])

    if not name:
        name = "data_analysis_report"

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    return f"{name}_{timestamp}.md"


def save_report(report: str, question: str) -> str:
    """
    Save the generated report inside the reports folder.
    """

    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True,
    )

    filename = create_report_filename(question)

    report_path = os.path.join(
        REPORT_FOLDER,
        filename,
    )

    with open(
        report_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(report)

    return report_path


def generate_sql_report(
    question: str,
    sql: str,
    result: list,
    answer: str,
) -> str:
    """
    Generate a professional human-readable SQL analysis report.
    """

    prompt = f"""
You are a senior data engineering reporting specialist.

Create a professional Markdown data analysis report.

User question:
{question}

SQL query:
{sql}

Query result:
{result}

Analysis:
{answer}

Create the report using this structure:

# Data Analysis Report

## Executive Summary

Briefly explain the result in simple language.

## Business Question

State the question being answered.

## Analysis Performed

Explain what was analyzed and what the query calculated.

## SQL Query

Show the SQL query inside a SQL code block.

## Results

Present the important results in a clean Markdown table
when multiple records are available.

If there is only one aggregate result, present it clearly
instead of creating an unnecessary table.

## Key Findings

List the important findings as bullet points.

## Conclusion

Give a concise conclusion based ONLY on the supplied
information.

Rules:

- Do not invent facts.
- Do not invent statistics.
- Do not add information not present in the query result.
- Do not return JSON.
- Do not mention this prompt.
- Do not mention being an AI.
- Use clean Markdown.
- Make the report easy for a human to read.
- Do not unnecessarily repeat the same information.
"""

    return ask_groq(prompt).strip()


def generate_profile_report(
    question: str,
    file_path: str,
    profile: dict,
    analysis: str,
) -> str:
    """
    Generate a professional human-readable data profiling report.
    """

    prompt = f"""
You are a senior data engineering reporting specialist.

Create a professional Markdown data profiling report.

User request:
{question}

File:
{file_path}

Dataset profile:
{profile}

Profile analysis:
{analysis}

Create the report using this structure:

# Data Profiling Report

## Executive Summary

Provide a short summary of the dataset and its overall
data quality based ONLY on the supplied information.

## Dataset Information

Include, when available:

- file
- processing mode
- number of rows
- number of columns
- column names

## Column Analysis

Present the columns and their data types in a clean
Markdown table.

## Data Quality

Discuss, when available:

- missing values
- empty values
- duplicate rows
- constant columns
- unique values
- other quality issues

Use tables where they improve readability.

## Statistical Summary

Include numeric statistics when available.

## Key Findings

List the important observations as bullet points.

## Recommendations

Provide practical data-engineering recommendations
based ONLY on the identified data-quality issues.

Do not invent problems that are not present.

## Conclusion

Provide a short conclusion.

Rules:

- Do not return JSON.
- Do not invent facts.
- Do not invent statistics.
- Do not mention this prompt.
- Do not mention being an AI.
- Use clean professional Markdown.
- Make the report easy to read.
- Avoid unnecessary repetition.
"""

    return ask_groq(prompt).strip()


def generate_and_save_sql_report(
    question: str,
    sql: str,
    result: list,
    answer: str,
) -> str:
    """
    Generate and save SQL report.
    """

    report = generate_sql_report(
        question=question,
        sql=sql,
        result=result,
        answer=answer,
    )

    return save_report(
        report=report,
        question=question,
    )


def generate_and_save_profile_report(
    question: str,
    file_path: str,
    profile: dict,
    analysis: str,
) -> str:
    """
    Generate and save profiling report.
    """

    report = generate_profile_report(
        question=question,
        file_path=file_path,
        profile=profile,
        analysis=analysis,
    )

    return save_report(
        report=report,
        question=question,
    )