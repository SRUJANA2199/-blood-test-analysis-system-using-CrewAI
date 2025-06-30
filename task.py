## Importing libraries and files
from crewai import Task

from agents import doctor, verifier, nutritionist, exercise_specialist
from tools import search_tool, read_data_tool, analyze_nutrition_tool, create_exercise_plan_tool

## Creating a task to help solve user's query
help_patients = Task(
    description="Analyze the blood test report and provide comprehensive medical insights based on the user's query: {query}. "
                "Read the blood test report carefully and identify key parameters, their values, and reference ranges. "
                "Provide accurate medical interpretation of the results and offer practical health recommendations. "
                "Focus on abnormal values and their potential clinical significance.",

    expected_output="""Provide a comprehensive blood test analysis including:
    - Summary of key blood parameters and their status (normal/abnormal)
    - Medical interpretation of significant findings
    - Health recommendations based on the results
    - Areas that may need medical attention
    - General wellness advice based on the blood work
    Format the response in clear sections with bullet points for easy reading.""",

    agent=doctor,
    tools=[read_data_tool, analyze_nutrition_tool, create_exercise_plan_tool],
    async_execution=False,
)

## Creating a nutrition analysis task
nutrition_analysis = Task(
    description="Analyze the blood test report focusing on nutrition-related parameters for query: {query}. "
                "Identify blood markers related to nutritional status such as hemoglobin, vitamins, minerals, and metabolic indicators. "
                "Provide specific dietary recommendations to address any deficiencies or imbalances found.",

    expected_output="""Provide detailed nutrition analysis including:
    - Nutrition-related blood parameters and their interpretation
    - Specific dietary recommendations for identified issues
    - Foods to include or avoid based on blood results
    - Supplement recommendations if appropriate
    - Meal planning suggestions tailored to the blood work findings""",

    agent=nutritionist,
    tools=[read_data_tool, analyze_nutrition_tool],
    async_execution=False,
)

## Creating an exercise planning task
exercise_planning = Task(
    description="Create an exercise plan based on the blood test results for query: {query}. "
                "Consider blood parameters that affect exercise capacity and safety such as hemoglobin, glucose, kidney function, and liver enzymes. "
                "Develop appropriate exercise recommendations that align with the person's health status.",

    expected_output="""Provide a comprehensive exercise plan including:
    - Exercise recommendations based on blood test findings
    - Intensity and duration guidelines appropriate for health status
    - Specific exercises to include or avoid based on blood parameters
    - Progression plan and safety considerations
    - Monitoring recommendations during exercise""",

    agent=exercise_specialist,
    tools=[read_data_tool, create_exercise_plan_tool],
    async_execution=False,
)

# Verification task
verification = Task(
    description="Verify that the uploaded document is a valid blood test report and extract key information. "
                "Ensure the document contains proper medical laboratory data and identify the main blood parameters tested.",

    expected_output="Confirm document type and provide summary of blood parameters found in the report. "
                    "List the main categories of tests performed and any notable findings that require attention.",

    agent=verifier,
    tools=[read_data_tool],
    async_execution=False
)
