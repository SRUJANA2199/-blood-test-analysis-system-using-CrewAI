import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tool
from langchain_community.document_loaders import PyPDFLoader

# PDF Reader Tool
@tool("Read and clean blood test report from a PDF file")
def read_data_tool(path: str = 'data/sample.pdf') -> str:
    """
    Tool to read and clean data from a PDF file.

    Args:
        path (str, optional): Path of the PDF file. Defaults to 'data/sample.pdf'.

    Returns:
        str: Cleaned and concatenated text from the PDF file.
    """
    try:
        loader = PyPDFLoader(file_path=path)
        docs = loader.load()

        full_report = ""
        for data in docs:
            content = data.page_content.replace("\n\n", "\n").strip()
            full_report += content + "\n"

        return full_report.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


# Nutrition Analysis Tool
@tool("Analyze blood report and recommend nutrition advice")
def analyze_nutrition_tool(blood_report_data: str) -> str:
    """
    Analyzes nutrition-related insights based on blood report text.

    Args:
        blood_report_data (str): Cleaned blood report text.

    Returns:
        str: Nutrition recommendations.
    """
    if "hemoglobin" in blood_report_data.lower():
        return "Hemoglobin appears low. Consider iron-rich foods like spinach, lentils, and red meat."
    elif "cholesterol" in blood_report_data.lower():
        return "High cholesterol detected. Recommend oats, nuts, and limiting fried food."
    else:
        return "General advice: Maintain a balanced diet with fruits, vegetables, lean protein, and whole grains."


# Exercise Planning Tool
@tool("Create exercise recommendations based on blood report")
def create_exercise_plan_tool(blood_report_data: str) -> str:
    """
    Generates exercise suggestions based on blood report indicators.

    Args:
        blood_report_data (str): Cleaned blood report text.

    Returns:
        str: Exercise plan suggestions.
    """
    if "glucose" in blood_report_data.lower():
        return "High glucose levels found. Suggest daily 30-minute walks and limiting sugary snacks."
    elif "blood pressure" in blood_report_data.lower() or "bp" in blood_report_data.lower():
        return "Elevated blood pressure. Recommend low-intensity activities like yoga and avoiding heavy lifting."
    else:
        return "Balanced fitness routine: Cardio (20 min/day) and strength training (3 times/week), with proper rest."

# Create tool class for easier import
class BloodTestReportTool:
    @staticmethod
    def read_data_tool(path: str = 'data/sample.pdf') -> str:
        return read_data_tool(path)
