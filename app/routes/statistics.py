from fastapi import APIRouter

from app.data import load_data

router = APIRouter()

@router.get("/patients/statistics")
def get_statistics():
    """Get overall statistics about patients"""
    data = load_data()
    
    if not data:
        return {"message": "No patients in database"}
    
    ages = []
    bmis = []
    gender_count = {"male": 0, "female": 0, "others": 0}
    city_count = {}
    
    for patient in data.values():
        ages.append(patient['age'])
        bmi = round(patient['weight'] / (patient['height'] ** 2), 2)
        bmis.append(bmi)
        
        gender_count[patient['gender']] = gender_count.get(patient['gender'], 0) + 1
        
        city = patient['city']
        city_count[city] = city_count.get(city, 0) + 1
    
    return {
        "total_patients": len(data),
        "age": {
            "average": round(sum(ages) / len(ages), 1),
            "min": min(ages),
            "max": max(ages)
        },
        "bmi": {
            "average": round(sum(bmis) / len(bmis), 1),
            "min": round(min(bmis), 1),
            "max": round(max(bmis), 1)
        },
        "gender_distribution": gender_count,
        "top_cities": sorted(city_count.items(), key=lambda x: x[1], reverse=True)[:5]
    }