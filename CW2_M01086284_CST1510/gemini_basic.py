import os
from dotenv import load_dotenv
import groq
import pandas as pd


class AIQueryManager:
    def __init__(self, api_env_path="api.env"):
        """
        Initialize the AIQueryManager, load API key, and create the client.
        """
        load_dotenv(api_env_path)
        self.api_key = os.getenv("GENAI_API_KEY")
        if not self.api_key:
            raise ValueError("GENAI_API_KEY not found in environment variables.")

        self.client = groq.Client(api_key=self.api_key)

        # System prompts for different domains
        self.system_prompts = {
            "cybersecurity": """
                You are a cybersecurity expert assistant.
                Analyze cyber incidents, detect threats, identify CVEs, IOCs, logs, malware, SIEM alerts, and MITRE ATT&CK techniques.
                Reply with technical, accurate explanations.
            """,
            "datascience": """
                You are a data science expert assistant.
                Help with statistics, EDA, charts, ML models, and data interpretation.
            """,
            "itops": """
                You are an IT operations expert assistant.
                Help troubleshoot systems, optimize performance, resolve tickets, and diagnose infrastructure issues.
            """
        }

    # -------------------------- Ask AI Directly --------------------------
    def ask_ai(self, domain: str, user_query: str) -> str:
        """
        Ask AI a question in a given domain.
        """
        if domain not in self.system_prompts:
            raise ValueError(f"Unknown domain: {domain}")

        prompt = self.system_prompts[domain] + "\nUser Query:\n" + user_query

        response = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    # -------------------------- Ask AI with Database Context --------------------------
    def query_database(self, domain: str, table_func, user_query: str, n_rows: int = 10) -> str:
        """
        Ask AI a question using the context of a table function that returns a DataFrame.

        Parameters:
        - domain: 'cybersecurity', 'datascience', 'itops'
        - table_func: function returning a DataFrame (get_all_incidents, get_all_datasets, get_all_tickets)
        - user_query: the question to ask
        - n_rows: number of rows from the DataFrame to include in context
        """
        if not callable(table_func):
            raise ValueError("table_func must be a callable that returns a pandas DataFrame.")

        df: pd.DataFrame = table_func()
        context = df.head(n_rows).to_string()
        prompt = f"Here is the recent data:\n{context}\n\nUser question:\n{user_query}"

        return self.ask_ai(domain, prompt)