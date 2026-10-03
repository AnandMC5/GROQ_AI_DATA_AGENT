#################### Project Setup #################
# from utils.groq_client import ask_groq

# def main():
#     print("=" * 50)
#     print("        GROQ DATA ENGINEERING AGENT")
#     print("=" * 50)

#     prompt = "Explain in one sentence what a data engineer does."

#     print("\nSending request to Groq...\n")

#     response = ask_groq(prompt)

#     print("Groq:")
#     print(response)


# if __name__ == "__main__":
#     main()

#########################################################


################### SUB AGENTS CALL ####################

# from utils.data_tools import profile_file
# from utils.large_data_tools import profile_large_file


# def main():
#     print("=" * 50)
#     print("        GROQ DATA ENGINEERING AGENT")
#     print("=" * 50)

#     #result = profile_file("data/input/customers.csv")
#     result = profile_file("data/input/orders.csv")    #It will use data_tools.py as the file size is less than <500
    
#     #result = profile_large_file("data/input/sales.psv")
#     #result = profile_large_file("data/input/product.xlsx")
    
#     print("\nDATA PROFILE")
#     print("-" * 50)

#     for key, value in result.items():
#         print(f"{key}: {value}")


# if __name__ == "__main__":
#     main()


####################### FROM ROUTER PROFILE AUTOMATICALLY SUB AGENTS BASED ON FILE SIZE ###############

# from utils.profile_router import profile_file

# def main():

#     print("=" * 50)
#     print("        GROQ DATA ENGINEERING AGENT")
#     print("=" * 50)

#     #result = profile_file("data/input/customers.csv")   #processing mode : samll file
#     #result = profile_file("data/input/sales.psv")       #processing mode : large file
     

#     print("\nDATA PROFILE")
#     print("-" * 50)

#     for key, value in result.items():
#         print(f"{key}: {value}")


# if __name__ == "__main__":
#     main()

######################### SQL AGENT SETUP & TEST ##############

# import os

# import psycopg2
# from dotenv import load_dotenv


# load_dotenv()


# POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
# POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# def main():

#     print("=" * 50)
#     print("       GROQ DATA ENGINEERING AGENT")
#     print("=" * 50)

#     print("\nConnecting to PostgreSQL...")

#     connection = psycopg2.connect(
#         host=POSTGRES_HOST,
#         port=POSTGRES_PORT,
#         database=POSTGRES_DATABASE,
#         user=POSTGRES_USER,
#         password=POSTGRES_PASSWORD,
#     )

#     print("PostgreSQL connection successful.")

#     cursor = connection.cursor()

#     cursor.execute("""
#         SELECT COUNT(*) AS total_users
#         FROM users;
#     """)

#     result = cursor.fetchone()

#     print(f"\nTotal users: {result[0]}")

#     cursor.close()
#     connection.close()

#     print("\nPostgreSQL connection closed.")


# if __name__ == "__main__":
#     main()


######################## 

############## GET TABLE STRUCTURE,COLUMNS DATA TYPE and SAMPLE ROWS from POSTGRES SCHEMA FOR GROQ understand the TABLE DATA #######

# from utils.sql_tools import get_database_schema


# def main():

#     print("=" * 60)
#     print("              DATABASE SCHEMA")
#     print("=" * 60)

#     database_schema = get_database_schema()

#     for table_name, table_info in database_schema.items():

#         print(f"\nTABLE: {table_name}")
#         print("-" * 40)

#         print("COLUMNS:")

#         for column in table_info["columns"]:
#             print(
#                 f"  {column['column_name']} "
#                 f"-> {column['data_type']}"
#             )

#         print("\nSAMPLE ROWS:")

#         for row in table_info["sample_rows"]:
#             print(row)


# if __name__ == "__main__":
#     main()
    
####################

###################### ASK SIMPLE QUESTIONS ON THOSE TABLE ################

# from agents.sql_agent import answer_question


# def main():

#     print("=" * 60)
#     print("             GROQ DATA ENGINEERING AGENT")
#     print("=" * 60)

#     question = input(
#         "\nAsk your database question: "
#     )

#     print("\nProcessing...")

#     response = answer_question(question)

#     print("\nGenerated SQL:")
#     print("-" * 60)
#     print(response["sql"])

#     print("\nQuery Result:")
#     print("-" * 60)
#     print(response["result"])

#     print("\nAnswer:")
#     print("-" * 60)
#     print(response["answer"])


# if __name__ == "__main__":
#     main()

###############################

##################### REPORT AGENT #############
# from agents.sql_agent import answer_question
# from agents.report_agent import generate_report


# def main():

#     print("=" * 60)
#     print("             GROQ DATA ENGINEERING AGENT")
#     print("=" * 60)

#     question = input(
#         "\nAsk your database question: "
#     )

#     print("\nProcessing...")

#     response = answer_question(question)

#     print("\nGenerated SQL:")
#     print("-" * 60)
#     print(response["sql"])

#     print("\nQuery Result:")
#     print("-" * 60)
#     print(response["result"])

#     print("\nAnswer:")
#     print("-" * 60)
#     print(response["answer"])

#     print("\nGenerating Report...")

#     report = generate_report(
#         question=question,
#         sql=response["sql"],
#         result=response["result"],
#         answer=response["answer"],
#     )

#     print("\nReport:")
#     print("=" * 60)
#     print(report)


# if __name__ == "__main__":
#     main()

####################################

######################### Calling Agent Based on Users Questions ###########

from agents.data_agent import run_data_agent
from agents.report_agent import (
    generate_and_save_sql_report,
    generate_and_save_profile_report,
)


def main():

    print("=" * 60)
    print("             GROQ DATA ENGINEERING AGENT")
    print("=" * 60)

    question = input("\nAsk your data question: ")

    print("\nProcessing...")

    response = run_data_agent(question)

    print("\nSelected Agent:")
    print("-" * 60)
    print(response["route"])

    # ==================================================
    # SQL AGENT
    # ==================================================

    if response["route"] == "SQL":

        sql_response = response["response"]

        print("\nGenerated SQL:")
        print("-" * 60)
        print(sql_response["sql"])

        print("\nQuery Result:")
        print("-" * 60)
        print(sql_response["result"])

        print("\nAnswer:")
        print("-" * 60)
        print(sql_response["answer"])

        print("\nGenerating Report...")
        print("-" * 60)

        report_path = generate_and_save_sql_report(
            question=question,
            sql=sql_response["sql"],
            result=sql_response["result"],
            answer=sql_response["answer"],
        )

        print("\nReport saved:")
        print("-" * 60)
        print(report_path)

    # ==================================================
    # PROFILE AGENT
    # ==================================================

    elif response["route"] == "PROFILE":

        if response["response"] is None:

            print("\nMessage:")
            print("-" * 60)
            print(response["message"])

            return

        profile_response = response["response"]

        print("\nFile:")
        print("-" * 60)
        print(profile_response["file_path"])

        print("\nProfile Result:")
        print("-" * 60)
        print(profile_response["profile"])

        print("\nAnalysis:")
        print("-" * 60)
        print(profile_response["analysis"])

        print("\nGenerating Report...")
        print("-" * 60)

        report_path = generate_and_save_profile_report(
            question=question,
            file_path=profile_response["file_path"],
            profile=profile_response["profile"],
            analysis=profile_response["analysis"],
        )

        print("\nReport saved:")
        print("-" * 60)
        print(report_path)


if __name__ == "__main__":
    main()