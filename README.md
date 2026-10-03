# GROQ_AI_DATA_AGENT
## 1. Project Structure:
The project is organized into modular agents, utilities, data, and report components.
It separates SQL analysis, data profiling, orchestration, and report generation for better maintainability.
The structure is designed to be scalable and easy to extend with additional data-engineering capabilities.
<img width="1536" height="1024" alt="project_structure_groq_ai_agent" src="https://github.com/user-attachments/assets/34c94e5f-6a0c-403f-8ef9-ec7ae9b9ec21" />

## 2. Profile Agent Output & Generated Report:
The Profile Agent automatically analyzes CSV, PSV, and XLSX datasets and identifies key data-quality information.
The terminal displays the profiling results and AI-generated insights during execution.
A detailed, human-readable Markdown report is automatically generated and stored in the reports/ folder.
<img width="959" height="539" alt="Screenshot 2026-10-03 204203" src="https://github.com/user-attachments/assets/f3827bff-2a22-4cc2-8b28-fd8512fabbf4" />

## 3. SQL Agent Output:
The SQL Agent converts natural-language questions into read-only PostgreSQL queries dynamically.
It analyzes the database results and generates a clear natural-language response.
The terminal shows the generated SQL, query results, and final analysis.
﻿<img width="959" height="547" alt="Screenshot 2026-10-03 201156" src="https://github.com/user-attachments/assets/f8f928b0-b5b4-4c70-a17c-8a4d56694c29" />

## 4. GROQ API:
Groq API Integration:
The project uses the Groq API to power its AI-driven SQL analysis, data profiling, and report generation.
The OpenAI-compatible API enables the agents to interact with the selected Groq language model.
This provides the intelligence layer for interpreting data and generating useful insights.
<img width="953" height="521" alt="Screenshot 2026-10-04 000952" src="https://github.com/user-attachments/assets/58c9ff90-7ce5-4177-98be-8bff963c5cd9" />


## 5. PostgreSQL Database:
PostgreSQL acts as the structured data source for the SQL Agent.
The agent dynamically discovers available tables, columns, and sample records before generating queries.
Only read-only SQL operations are performed to safely retrieve and analyze database information.
<img width="956" height="535" alt="Screenshot 2026-10-04 001825" src="https://github.com/user-attachments/assets/affc0323-2c59-4522-8ef4-a6bbbf3a471c" />
