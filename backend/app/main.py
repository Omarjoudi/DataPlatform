from fastapi import FastAPI
from app.api import tasks
from app.api import campaigns

app = FastAPI(
    title="DP Backend API",
    description="Backend for the Dash frontend, powered by FastAPI",
    version="1.0.0",
)

app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["Campaigns"])

@app.get("/")
def health_check():
    """
    A simple health check endpoint to verify the API is running.
    """
    return {
        "status": "success", 
        "message": "FastAPI is up and running!"
    }



