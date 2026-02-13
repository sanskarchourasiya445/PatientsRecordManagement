from fastapi import APIRouter, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List

from app.models import Patient
from app.schemas import PatientUpdate
from app.data import load_data, save_data  

router = APIRouter()

@router.get("/patients")
def view():
    data = load_data()
    return data

@router.get('/patients/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    data = load_data()

    if patient_id in data:
        patient_data = data[patient_id]
        patient_data['id'] = patient_id  # ID add karo
        return patient_data
    raise HTTPException(status_code=404, detail='Patient not found')

@router.get('/patients/sort')
def sort_patients(
    sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'),
    order: str = Query('asc', description='sort in asc or desc order')
):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()
    
    # BMI calculate karo for sorting
    patients_list = []
    for pid, pdata in data.items():
        pdata_copy = pdata.copy()
        pdata_copy['id'] = pid
        # BMI calculate manually for sorting
        bmi = round(pdata['weight'] / (pdata['height'] ** 2), 2)
        pdata_copy['bmi'] = bmi
        patients_list.append(pdata_copy)

    reverse = True if order == 'desc' else False
    sorted_data = sorted(patients_list, key=lambda x: x.get(sort_by, 0), reverse=reverse)

    return sorted_data

@router.post('/patients', status_code=201)
def create_patient(patient: Patient):
    try:
        print(f"Creating patient: {patient.id}")
        data = load_data()

        if patient.id in data:
            raise HTTPException(status_code=400, detail='Patient already exists')
        
        # Save without id and computed fields
        data[patient.id] = {
            'name': patient.name,
            'city': patient.city,
            'age': patient.age,
            'gender': patient.gender,
            'height': float(patient.height),
            'weight': float(patient.weight)
        }

        save_data(data)
        print(f"Patient {patient.id} created successfully")
        
        return JSONResponse(
            status_code=201, 
            content={
                'message': 'patient created successfully',
                'patient_id': patient.id
            }
        )
    except Exception as e:
        print(f"Error creating patient: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")

@router.put('/patients/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    try:
        print(f"Updating patient: {patient_id}")
        print(f"Update data: {patient_update}")
        
        data = load_data()

        if patient_id not in data:
            raise HTTPException(status_code=404, detail='Patient not found')
        
        # Get existing data (copy to avoid reference issues)
        existing_data = data[patient_id].copy()
        print(f"Existing data: {existing_data}")
        
        # Get update data
        update_data = patient_update.model_dump(exclude_unset=True)
        print(f"Update data: {update_data}")
        
        # Apply updates
        for key, value in update_data.items():
            existing_data[key] = value
        
        # Ensure correct types
        patient_dict = {
            'id': patient_id,
            'name': str(existing_data['name']),
            'city': str(existing_data['city']),
            'age': int(existing_data['age']),
            'gender': str(existing_data['gender']),
            'height': float(existing_data['height']),
            'weight': float(existing_data['weight'])
        }
        
        # Validate with Patient model
        patient_obj = Patient(**patient_dict)
        print(f"Validated patient: BMI={patient_obj.bmi}, Verdict={patient_obj.verdict}")
        
        # Save without id and computed fields
        data[patient_id] = {
            'name': patient_obj.name,
            'city': patient_obj.city,
            'age': patient_obj.age,
            'gender': patient_obj.gender,
            'height': patient_obj.height,
            'weight': patient_obj.weight
        }
        
        save_data(data)
        print(f"Patient {patient_id} updated successfully")
        
        return JSONResponse(
            status_code=200, 
            content={
                'message': 'patient updated successfully',
                'patient_id': patient_id
            }
        )
    except HTTPException:
        raise
    except KeyError as e:
        print(f"KeyError: {e}")
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid value: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")

@router.delete('/patients/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient deleted successfully'})