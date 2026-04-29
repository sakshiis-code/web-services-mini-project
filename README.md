# Student Result + Country Enrichment REST API

## 📌 Project Overview
This project is a Flask-based REST API for managing student records.

It supports:
- CRUD operations
- API key security
- External REST API integration
- JSON responses
- Postman testing

The API enriches student data using the RestCountries API.

---

## 🚀 Technologies Used
- Python
- Flask
- Requests
- REST API
- Postman

---

## 🔐 Security
API key authentication using custom headers.

Header:
X-API-Key: key_student_001

---

## 🌍 External API Used
https://restcountries.com/

Used for fetching:
- Capital
- Population
- Currency

---

## 📦 Endpoints

### GET /students
Get all students

### GET /students/{rollNo}
Get student with live country info

### POST /students
Add new student

### PUT /students/{rollNo}/marks
Update marks

### DELETE /students/{rollNo}
Delete student

---

## ▶️ Run Project

Install dependencies:

```bash
pip install flask requests
```

Run:

```bash
py mini_project.py
```

Server:
http://localhost:5000