import json

def load_data():
    try:
        with open('patients.json','r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f,indent=4)