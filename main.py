
# Import FastAPI framework and request helpers
from fastapi import FastAPI, File, UploadFile, Form, HTTPException

# Standard libraries for file handling and async workflow
import os, uuid, asyncio

# CrewAI orchestration components
from crewai import Crew, Process

# Import agent and task definitions
from agents import financial_analyst
from task import analyze_financial_document


# Create FastAPI application instance
app = FastAPI(title="Financial Document Analyzer")


# Function to run CrewAI workflow
def run_crew(query: str, file_path: str="data/sample.pdf"):
    """Run the CrewAI workflow with given query and document path"""

    # Create Crew with agent + task
    financial_crew = Crew(
        agents=[financial_analyst],             # Agent that will perform reasoning
        tasks=[analyze_financial_document],     # Task defining what to do
        process=Process.sequential,             # Execute tasks sequentially
    )

    # Start execution and pass inputs to task
    result = financial_crew.kickoff({'query': query, 'file_path': file_path})

    return result


# Root endpoint (health check)
@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}


# Main API endpoint for document analysis
@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),  # PDF uploaded by user
    query: str = Form(default="Analyze this financial document for investment insights")  # User query
):
    """Analyze financial document and provide comprehensive investment recommendations"""

    # Create unique file name for uploaded document
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded PDF to disk
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate query text
        if query == "" or query is None:
            query = "Analyze this financial document for investment insights"

        # Run CrewAI workflow using uploaded file
        response = run_crew(query=query.strip(), file_path=file_path)

        # Return response to API client
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    # Catch and return runtime errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

    # Cleanup uploaded file after processing
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors


# Allow running file directly without CLI uvicorn command
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)