# 🏥 Patient Record Management System API

A powerful and efficient RESTful API built with **FastAPI** for managing patient records with automatic BMI calculation and health verdict.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

---

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [API Endpoints](#-api-endpoints)
- [Example Requests](#-example-requests)
- [Data Models](#-data-models)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

✅ **Complete CRUD Operations** - Create, Read, Update, Delete patients  
✅ **Automatic BMI Calculation** - BMI calculated automatically from height & weight  
✅ **Health Verdict** - Underweight, Normal, Overweight, Obese  
✅ **Advanced Search** - Search by name, city, age range, gender  
✅ **Statistics Dashboard** - Get overall patient statistics  
✅ **Sorting** - Sort patients by height, weight, or BMI  
✅ **Data Persistence** - JSON file-based storage  
✅ **Input Validation** - Pydantic models ensure data integrity  
✅ **Interactive Documentation** - Auto-generated Swagger UI  

---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.13
- **Data Validation**: Pydantic v2
- **Data Storage**: JSON file
- **Documentation**: Swagger UI / ReDoc

---

## 📁 Project Structure

```text
patient-management-system/
├── app/
│ ├── init.py
│ ├── main.py # Main FastAPI application
│ ├── models.py # Pydantic models (Patient class)
│ ├── schemas.py # Request/Response schemas
│ ├── data.py # JSON file operations
│ └── routes/ # API endpoints
│ ├── init.py
│ ├── patients.py # Patient CRUD operations
│ ├── statistics.py # Statistics endpoints
│ └── search.py # Search endpoints
├── patients.json # Data storage file
├── requirements.txt # Dependencies
└── README.md # Documentation

```
###🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/sanskarchourasiya445/PatientsRecordManagement.git
cd PatientsRecordManagement
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Application

```bash
uvicorn app.main:app --reload
```

The server will start at: **http://127.0.0.1:8000**

---

## 📚 API Documentation

Once the application is running, you can access:

| Documentation | URL |
|--------------|-----|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |

---

## 🔌 API Endpoints

### Basic Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/about` | API information |
| GET | `/health` | Health check |

### Patient Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/view` | Get all patients |
| GET | `/patient/{patient_id}` | Get specific patient |
| POST | `/create` | Create new patient |
| PUT | `/edit/{patient_id}` | Update patient |
| DELETE | `/delete/{patient_id}` | Delete patient |
| GET | `/sort` | Sort patients (height/weight/bmi) |

### Statistics & Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/statistics` | Get overall statistics |
| GET | `/search` | Advanced patient search |

---

## 📝 Example Requests

### 1. Create a New Patient
```bash
curl -X POST http://127.0.0.1:8000/create \
  -H "Content-Type: application/json" \
  -d '{
    "id": "P001",
    "name": "John Doe",
    "city": "New York",
    "age": 30,
    "gender": "male",
    "height": 1.75,
    "weight": 70
  }'
```

**Response:**
```json
{
  "message": "patient created successfully",
  "patient_id": "P001"
}
```

### 2. Get All Patients
```bash
curl -X GET http://127.0.0.1:8000/view
```

**Response:**
```json
{
  "P001": {
    "name": "John Doe",
    "city": "New York",
    "age": 30,
    "gender": "male",
    "height": 1.75,
    "weight": 70
  }
}
```

### 3. Get Specific Patient
```bash
curl -X GET http://127.0.0.1:8000/patient/P001
```

### 4. Update Patient
```bash
curl -X PUT http://127.0.0.1:8000/edit/P001 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "age": 31,
    "city": "Los Angeles"
  }'
```

### 5. Delete Patient
```bash
curl -X DELETE http://127.0.0.1:8000/delete/P001
```

### 6. Sort Patients
```bash
# Sort by BMI in descending order
curl -X GET "http://127.0.0.1:8000/sort?sort_by=bmi&order=desc"
```

### 7. Search Patients
```bash
# Search by city and age range
curl -X GET "http://127.0.0.1:8000/search?city=New%20York&min_age=25&max_age=35"
```

### 8. Get Statistics
```bash
curl -X GET http://127.0.0.1:8000/statistics
```

**Response:**
```json
{
  "total_patients": 5,
  "age": {
    "average": 32.5,
    "min": 25,
    "max": 45
  },
  "bmi": {
    "average": 24.3,
    "min": 18.5,
    "max": 31.2
  },
  "gender_distribution": {
    "male": 3,
    "female": 2,
    "others": 0
  },
  "top_cities": [
    ["New York", 2],
    ["Los Angeles", 2],
    ["Chicago", 1]
  ]
}
```

---

## 📊 Data Models

### Patient Model
```json
{
  "id": "string (required, unique)",
  "name": "string (2-50 chars, required)",
  "city": "string (required)",
  "age": "integer (1-119, required)",
  "gender": "enum [male, female, others]",
  "height": "float (>0, in meters)",
  "weight": "float (>0, in kgs)",
  "bmi": "float (auto-calculated)",
  "verdict": "string (auto-calculated)"
}
```

### BMI Categories
| BMI Range | Category |
|-----------|----------|
| < 18.5 | Underweight |
| 18.5 - 24.9 | Normal |
| 25 - 29.9 | Overweight |
| ≥ 30 | Obese |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a new branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

**Happy Coding!** 🚀
