
from flask import Flask, jsonify, request

app = Flask(__name__)

students = [
    {"id": 1, "name": "Alice", "age": 20},
    {"id": 2, "name": "Bob", "age": 22},
    {"id": 3, "name": "Charlie", "age": 21}
]


@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200


@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data or 'name' not in data or 'age' not in data:
        return jsonify({"error": "Name and age are required"}), 400

    new_id = max((s['id'] for s in students), default=0) + 1

    new_student = {
        "id": new_id,
        "name": data['name'],
        "age": data['age']
    }

    students.append(new_student)
    return jsonify(new_student), 201


@app.route('/students/<int:student_id>', methods=['PATCH'])
def update_student(student_id):
    data = request.get_json() or {}

    for student in students:
        if student['id'] == student_id:
            if 'name' in data:
                student['name'] = data['name']
            if 'age' in data:
                student['age'] = data['age']

            return jsonify(student), 200

    return jsonify({"error": "Student not found"}), 404


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students

    for student in students:
        if student['id'] == student_id:
            students = [
                s for s in students if s['id'] != student_id
            ]
            return jsonify({"message": "Student deleted"}), 200

    return jsonify({"error": "Student not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=3000)
