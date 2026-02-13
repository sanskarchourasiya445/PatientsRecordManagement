from fastapi import APIRouter, Query
from typing import Optional, Literal

from app.data import load_data

router = APIRouter()

@router.get('/patients/search')
def search_patients(
    name: Optional[str] = Query(None, description="Search by name (partial match)"),
    city: Optional[str] = Query(None, description="Filter by city"),
    min_age: Optional[int] = Query(None, ge=0, le=120, description="Minimum age"),
    max_age: Optional[int] = Query(None, ge=0, le=120, description="Maximum age"),
    gender: Optional[Literal['male', 'female', 'others']] = Query(None, description="Filter by gender")
):
    """Advanced search with multiple filters"""
    data = load_data()
    results = []
    
    for patient_id, patient in data.items():
        # Start with all patients, then apply filters
        match = True
        
        if name and name.lower() not in patient['name'].lower():
            match = False
        
        if city and city.lower() != patient['city'].lower():
            match = False
        
        if min_age and patient['age'] < min_age:
            match = False
            
        if max_age and patient['age'] > max_age:
            match = False
            
        if gender and patient['gender'] != gender:
            match = False
        
        if match:
            patient_copy = patient.copy()
            patient_copy['id'] = patient_id
            # Calculate BMI for each result
            bmi = round(patient['weight'] / (patient['height'] ** 2), 2)
            patient_copy['bmi'] = bmi
            results.append(patient_copy)
    
    return {
        "count": len(results),
        "filters_applied": {
            "name": name,
            "city": city,
            "min_age": min_age,
            "max_age": max_age,
            "gender": gender
        },
        "results": results
    }