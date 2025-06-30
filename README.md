# -blood-test-analysis-system-using-CrewAI


# Features
•	PDF Upload:      
•	Multi-Specialist Analysis:   
o	Medical doctor analysis with health recommendations       
o	Nutritionist advice based on blood markers       
o	Exercise physiologist workout planning       
•	Interactive Web Interface        
•	Real-Time Analysis            


# Bugs Found and Fixes Applied
1.	FastAPI Server Startup Issues   
Problem: Server failed to start due to missing static file configuration and import errors.  
Fix Applied:  
•	Added StaticFiles import and mounted static directory  
•	Configured / route to serve the frontend interface

3.	CrewAI Import Errors   
 Problem : encountered CrewAI import errors mostly due to incorrect or outdated module references, missing packages, or incorrect usage of decorators and tools.  
Fixes applied:  
Some of them are  
ImportError: cannot import name 'tool' from 'crewai_tools'  
But tool should be imported from the right submodule.  

ModuleNotFoundError: No module named 'crewai_tools.tool'  
•	This means crewai_tools was installed, but the tool module wasn’t accessible — often due to:  
o	Incorrect version of the package  
o	Improper installation  

3. Missing Frontend Interface  
Problem: Application only provided API endpoints without user interface.  
Fix Applied:  
•	Created complete HTML frontend with CSS styling  
•	Implemented drag-and-drop file upload functionality  
•	Added JavaScript for API communication and result display  

4.PDF Processing   
Problem: PDF text extraction was not properly handling different blood test formats.  
Fix Applied:  
•	Enhanced PDF text extraction with regex patterns  

5.Analysis Output format  
Problem: Analysis results were not properly structured for frontend display.  
Fix Applied:  
•	Added bullet-point formatting for recommendations  
•	Made the output format with clear section headers  


# Setup and usage instructions
Prerequisites
•	Python 3.11 or higher  
•	pip package manager  
Install dependencies:  
pip install fastapi uvicorn pypdf python-dotenv python-multipart langchain-community  
Verify project structure:    
├── main.py                 # FastAPI application  
├── tools.py               # PDF processing tools  
├── static/  
│   └── index.html         # Web frontend  
├── data/  
│   └── sample.pdf         # Sample blood test  
└── README.md  

Start the server:  
python main.py  

Access the application:    
•	Open your browser and go to: http://localhost:8000    
•	Upload a blood test PDF and get instant analysis    


# Usage Instructions  
Web Interface
1.	Upload PDF: Drag and drop your blood test PDF or click to browse
2.	Analyze: Click "Analyze Blood Report" button
3.	View Results: Review the three specialist analyses:  
•	Medical Analysis (health recommendations)  
•	Nutritional Recommendations (diet advice)  
•	Exercise Plan (workout suggestions)  
API Endpoints  
•	GET /: Serves the web frontend  
•	POST /analyze: Analyzes uploaded blood test PDF  
•	GET /api: API health check  
•	GET /test-sample: Tests analysis with sample PDF  
# API Documentation  
POST /analyze
Analyzes an uploaded blood test PDF file.
Request:
•	Method: POST
•	Content-Type: multipart/form-data
•	Parameters:
o	file (required): PDF file of blood test report
o	query (optional): Analysis query (default: "Summarise my Blood Test Report")  
Response:  
{  
  "status": "success",  
  "analysis": "MEDICAL ANALYSIS\n • Health recommendation 1\n • Health recommendation 2\n\nNUTRITIONAL RECOMMENDATIONS\n • Nutrition advice 1\n • Nutrition advice   2\n\nEXERCISE PLAN\n • Exercise suggestion 1\n • Exercise suggestion 2",  
  "file_name": "blood_test.pdf"  
}  
Error Response:  
{  
  "status": "error",  
  "detail": "Error message description"  
}  
GET /test-sample  
Tests the analysis system with the included sample PDF.  
Response:  
{  
  "status": "success",  
  "analysis": "Complete analysis of sample blood test...",  
  "file_name": "sample.pdf"  
}  
GET /api  
Health check endpoint for the API.  
Response:  
{  
  "message": "Blood Test Report Analyser API is running"  
}  
  





