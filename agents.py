## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM
from tools import search_tool, read_data_tool, analyze_nutrition_tool, create_exercise_plan_tool

# Load your model (huggingface inference or local Ollama etc.)
llm = LLM(
    model=os.getenv("LLM_MODEL", "huggingface/meta-llama/Meta-Llama-3.1-8B-Instruct")
)

# Agent: Doctor
doctor = Agent(
    role="Senior Medical Doctor",
    goal="Analyze blood test reports and provide comprehensive medical insights and recommendations.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced medical doctor with expertise in interpreting blood test results. "
        "You provide accurate medical analysis based on laboratory values and reference ranges. "
        "You offer practical health recommendations while being careful not to replace direct medical consultation. "
        "You analyze blood parameters systematically and provide evidence-based advice."
    ),
    tools=[read_data_tool, analyze_nutrition_tool, create_exercise_plan_tool],
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=True
)

# Agent: Verifier
verifier = Agent(
    role="Medical Report Verifier",
    goal="Verify that uploaded documents are valid blood test reports and extract key medical information.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a medical records specialist who validates blood test reports. "
        "You ensure documents contain proper medical laboratory data and identify key blood parameters. "
        "You have experience in recognizing various blood test formats and medical terminology."
    ),
    tools=[read_data_tool],
    llm=llm,
    max_iter=1,
    max_rpm=10,
    allow_delegation=False
)

# Agent: Nutritionist
nutritionist = Agent(
    role="Clinical Nutritionist",
    goal="Provide evidence-based nutrition recommendations based on blood test results.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified clinical nutritionist with expertise in interpreting blood work for dietary recommendations. "
        "You understand how various blood parameters relate to nutritional status and metabolic health. "
        "You provide practical, science-based nutrition advice tailored to individual blood test results."
    ),
    tools=[read_data_tool, analyze_nutrition_tool],
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

# Agent: Exercise Specialist
exercise_specialist = Agent(
    role="Exercise Physiologist",
    goal="Create safe and effective exercise recommendations based on blood test indicators.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified exercise physiologist who specializes in creating fitness plans based on health indicators. "
        "You understand how blood parameters relate to exercise capacity and safety considerations. "
        "You provide tailored exercise recommendations that consider individual health status and limitations."
    ),
    tools=[read_data_tool, create_exercise_plan_tool],
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)
