
## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

# search tool
search_tool = SerperDevTool()


# PDF reader tool
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads a financial PDF document and returns text"

    def _run(self, path: str = "data/sample.pdf") -> str:
        docs = PyPDFLoader(path).load()

        full_report = ""
        for data in docs:
            content = data.page_content

            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content + "\n"

        return full_report


class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data):
        return "Investment analysis functionality to be implemented"


class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data):
        return "Risk assessment functionality to be implemented"