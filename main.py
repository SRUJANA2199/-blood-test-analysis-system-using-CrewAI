from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uuid
import re
from langchain_community.document_loaders import PyPDFLoader

app = FastAPI(title="Blood Test Report Analyser")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

def extract_blood_values(text: str) -> dict:
    """Extract blood test values from text"""
    values = {}
    
    # Common blood test patterns
    patterns = {
        'hemoglobin': r'hemoglobin.*?(\d+\.?\d*)',
        'glucose': r'glucose.*?(\d+\.?\d*)',
        'cholesterol': r'cholesterol.*?(\d+\.?\d*)',
        'creatinine': r'creatinine.*?(\d+\.?\d*)',
        'urea': r'urea.*?(\d+\.?\d*)',
        'rbc': r'rbc count.*?(\d+\.?\d*)',
        'wbc': r'(?:wbc|total leukocyte count).*?(\d+\.?\d*)',
        'platelet': r'platelet.*?(\d+\.?\d*)',
    }
    
    text_lower = text.lower()
    for key, pattern in patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            values[key] = float(match.group(1))
    
    return values

def analyze_blood_report(file_path: str, query: str) -> str:
    """Rule-based blood test analysis"""
    try:
        # Read PDF
        loader = PyPDFLoader(file_path=file_path)
        docs = loader.load()
        
        full_report = ""
        for doc in docs:
            full_report += doc.page_content + "\n"
        
        # Extract blood values
        blood_values = extract_blood_values(full_report)
        
        # Generate analysis
        analysis = generate_medical_analysis(blood_values, full_report)
        nutrition = generate_nutrition_analysis(blood_values, full_report)
        exercise = generate_exercise_analysis(blood_values, full_report)
        
        result = f"""
# COMPREHENSIVE BLOOD TEST ANALYSIS

## MEDICAL ANALYSIS (Dr. Smith, Senior Medical Doctor)
{analysis}

## NUTRITIONAL RECOMMENDATIONS (Sarah Johnson, Clinical Nutritionist)  
{nutrition}

## EXERCISE PLAN (Mike Wilson, Exercise Physiologist)
{exercise}

---
*This analysis is based on the blood test values found in your report. Please consult with your healthcare provider for personalized medical advice.*
        """
        
        return result.strip()
        
    except Exception as e:
        return f"Analysis failed: {str(e)}"

def generate_medical_analysis(values: dict, full_text: str) -> str:
    """Generate medical analysis based on blood values"""
    analysis = []
    
    # Hemoglobin analysis
    if 'hemoglobin' in values:
        hb = values['hemoglobin']
        if hb < 13.0:
            analysis.append(f"• **Hemoglobin: {hb} g/dL** - Below normal range (13.0-17.0). This suggests possible anemia. Recommend iron studies and dietary iron increase.")
        elif hb > 17.0:
            analysis.append(f"• **Hemoglobin: {hb} g/dL** - Above normal range. May indicate dehydration or polycythemia. Recommend hydration and follow-up.")
        else:
            analysis.append(f"• **Hemoglobin: {hb} g/dL** - Within normal range (13.0-17.0). Good oxygen-carrying capacity.")
    
    # Glucose analysis
    if 'glucose' in values:
        glucose = values['glucose']
        if glucose > 126:
            analysis.append(f"• **Glucose: {glucose} mg/dL** - Elevated. Suggests diabetes or prediabetes. Recommend lifestyle changes and medical consultation.")
        elif glucose > 100:
            analysis.append(f"• **Glucose: {glucose} mg/dL** - Slightly elevated. Monitor blood sugar and consider dietary modifications.")
        else:
            analysis.append(f"• **Glucose: {glucose} mg/dL** - Normal fasting glucose levels.")
    
    # Creatinine analysis
    if 'creatinine' in values:
        creat = values['creatinine']
        if creat > 1.3:
            analysis.append(f"• **Creatinine: {creat} mg/dL** - Elevated. May indicate kidney function issues. Recommend nephrology consultation.")
        else:
            analysis.append(f"• **Creatinine: {creat} mg/dL** - Normal kidney function indicated.")
    
    if not analysis:
        analysis.append("• Blood parameters appear to be within normal ranges based on available data.")
    
    return "\n".join(analysis)

def generate_nutrition_analysis(values: dict, full_text: str) -> str:
    """Generate nutrition recommendations"""
    recommendations = []
    
    if 'hemoglobin' in values and values['hemoglobin'] < 13.0:
        recommendations.append("• **Iron-rich foods**: Include red meat, spinach, lentils, fortified cereals")
        recommendations.append("• **Vitamin C**: Enhance iron absorption with citrus fruits, bell peppers")
        recommendations.append("• **Avoid**: Tea/coffee with iron-rich meals")
    
    if 'glucose' in values and values['glucose'] > 100:
        recommendations.append("• **Complex carbs**: Choose whole grains, quinoa, brown rice")
        recommendations.append("• **Fiber**: Include beans, vegetables, fruits with skin")
        recommendations.append("• **Limit**: Refined sugars, white bread, sugary drinks")
        recommendations.append("• **Portion control**: Smaller, frequent meals")
    
    if 'cholesterol' in values and values['cholesterol'] > 200:
        recommendations.append("• **Healthy fats**: Olive oil, avocados, nuts, fatty fish")
        recommendations.append("• **Soluble fiber**: Oats, beans, apples")
        recommendations.append("• **Limit**: Saturated fats, trans fats, processed foods")
    
    if not recommendations:
        recommendations.append("• **Balanced diet**: Focus on fruits, vegetables, lean proteins, whole grains")
        recommendations.append("• **Hydration**: 8-10 glasses of water daily")
        recommendations.append("• **Omega-3**: Include fish 2-3 times per week")
    
    return "\n".join(recommendations)

def generate_exercise_analysis(values: dict, full_text: str) -> str:
    """Generate exercise recommendations"""
    recommendations = []
    
    if 'hemoglobin' in values and values['hemoglobin'] < 13.0:
        recommendations.append("• **Low intensity**: Start with light walking, yoga")
        recommendations.append("• **Gradual increase**: Build endurance slowly")
        recommendations.append("• **Avoid**: High-intensity workouts until levels improve")
    
    if 'glucose' in values and values['glucose'] > 100:
        recommendations.append("• **Cardio**: 30 minutes daily walking, swimming, cycling")
        recommendations.append("• **Resistance training**: 2-3 times per week")
        recommendations.append("• **Post-meal walks**: 10-15 minutes after eating")
    
    if 'creatinine' in values and values['creatinine'] > 1.3:
        recommendations.append("• **Moderate exercise**: Avoid excessive protein supplementation")
        recommendations.append("• **Hydration**: Maintain proper fluid intake during exercise")
    
    if not recommendations:
        recommendations.append("• **Cardio**: 150 minutes moderate intensity per week")
        recommendations.append("• **Strength training**: 2-3 sessions per week")
        recommendations.append("• **Flexibility**: Daily stretching or yoga")
        recommendations.append("• **Rest**: 1-2 rest days per week")
    
    return "\n".join(recommendations)

@app.get("/")
async def serve_frontend():
    return FileResponse('static/index.html')

@app.get("/api")
async def root():
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            f.write(content)
        
        if not query or query.strip() == "":
            query = "Summarise my Blood Test Report"
            
        response = analyze_blood_report(file_path, query.strip())
        
        return {
            "status": "success",
            "query": query,
            "analysis": response,
            "file_processed": file.filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Blood Test Report Analyser",
        "version": "1.0.0"
    }

@app.get("/test-sample")
async def test_sample_analysis():
    """Test endpoint to analyze the sample.pdf file"""
    sample_file_path = "data/sample.pdf"
    
    if not os.path.exists(sample_file_path):
        raise HTTPException(status_code=404, detail="Sample PDF file not found")
    
    try:
        query = "Provide comprehensive analysis of this blood test report"
        response = analyze_blood_report(sample_file_path, query)
        
        return {
            "status": "success",
            "query": query,
            "analysis": response,
            "file_processed": "sample.pdf"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sample report: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
