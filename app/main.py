from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routes import patients_router, statistics_router, search_router
from app.data import load_data
app = FastAPI()

# Include all routers
app.include_router(patients_router)
app.include_router(statistics_router)
app.include_router(search_router)

@app.get("/")
def Patients_Record():
    return {
        "message": "Welcome to the Patient Record Management System API",
        "version": "1.0.0",
        "docs": "/docs"
        "framework": "FastAPI",
        "features": [
            "Create Patient Records",
            "View All Patients",
            "Search & Filter Patients",
            "Sort Patients",
            "Update Patient Details",
            "Delete Patient Records",
            "Patient Health Statistics"
        ],
    }

@app.get("/about")
def about():
    return {
        "project": "Patients Record Management System",
        "features": [
            "CRUD Operations",
            "Search & Filter",
            "Sorting",
            "Statistics"
        ]
    }


# Health check endpoint (optional)
@app.get("/health")
def health_check():
    try:
        data = load_data()
        return {
            "status": "healthy",
            "patients_count": len(data)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )
