from flask import Flask, request, jsonify
import requests
from functools import wraps

app = Flask(__name__)

@app.route('/')
def home():
    return "Student REST API is Running!"

# ── API Keys ─────────────────────────────
VALID_KEYS = {
    "key_student_001",
    "key_faculty_999"
}

# ── External API ─────────────────────────
COUNTRY_API = "https://restcountries.com/v3.1/name/{}"

# ── In-memory Database ───────────────────
students = {
    "CS001": {
        "name": "Priya Sharma",
        "marks": 87,
        "country": "India"
    },
    "CS002": {
        "name": "Yuki Tanaka",
        "marks": 92,
        "country": "Japan"
    },
    "CS003": {
        "name": "Lena Mueller",
        "marks": 78,
        "country": "Germany"
    }
}

# ── API Key Authentication ───────────────
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")

        if key not in VALID_KEYS:
            return jsonify({
                "error": "Unauthorized"
            }), 401

        return f(*args, **kwargs)

    return decorated

# ── External API Function ────────────────
def get_country_info(country_name):

    try:
        response = requests.get(
            COUNTRY_API.format(country_name.lower()),
            timeout=5
        )

        if response.status_code == 200:

            data = response.json()[0]

            return {
                "capital":
                    data.get("capital", ["N/A"])[0],

                "population":
                    data.get("population", 0),

                "currency":
                    list(
                        data.get("currencies", {}).keys()
                    )[0]
                    if data.get("currencies")
                    else "N/A"
            }

    except Exception:
        pass

    return {
        "capital": "N/A",
        "population": 0,
        "currency": "N/A"
    }

# ── GET All Students ─────────────────────
@app.route('/students', methods=['GET'])
@require_api_key
def get_students():

    return jsonify(students), 200

# ── GET One Student ──────────────────────
@app.route('/students/<roll_no>', methods=['GET'])
@require_api_key
def get_student(roll_no):

    student = students.get(roll_no)

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    # Country API Call
    country_info = get_country_info(
        student["country"]
    )

    enriched_data = {
        **student,
        "country_details": country_info
    }

    return jsonify(enriched_data), 200

# ── POST Add Student ─────────────────────
@app.route('/students', methods=['POST'])
@require_api_key
def add_student():

    data = request.get_json()

    roll = data.get("rollNo")

    if not roll or roll in students:
        return jsonify({
            "error":
            "Invalid or duplicate roll number"
        }), 400

    students[roll] = {
        "name":
            data.get("name", "Unknown"),

        "marks":
            data.get("marks", 0),

        "country":
            data.get("country", "India")
    }

    return jsonify({
        "message": "Student added",
        "rollNo": roll
    }), 201

# ── PUT Update Marks ─────────────────────
@app.route('/students/<roll_no>/marks',
           methods=['PUT'])
@require_api_key
def update_marks(roll_no):

    if roll_no not in students:
        return jsonify({
            "error": "Student not found"
        }), 404

    data = request.get_json()

    students[roll_no]["marks"] = data.get(
        "marks",
        students[roll_no]["marks"]
    )

    return jsonify(students[roll_no]), 200

# ── DELETE Student ───────────────────────
@app.route('/students/<roll_no>',
           methods=['DELETE'])
@require_api_key
def delete_student(roll_no):

    if roll_no not in students:
        return jsonify({
            "error": "Student not found"
        }), 404

    del students[roll_no]

    return jsonify({
        "message": f"{roll_no} deleted"
    }), 200

# ── Main ─────────────────────────────────
if __name__ == '__main__':

    print("Server running on:")
    print("http://localhost:5000")

    app.run(
        debug=True,
        port=5000
    )