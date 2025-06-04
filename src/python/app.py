from flask import Flask, jsonify, request, send_file
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Абсолютний шлях до БД
DB_PATH = r"E:\Lab_6_BD\src\sql\lab6.db"


@app.route('/')
def serve_interface():
    return send_file('index.html')


def query_db(query, args=(), one=False, commit=False):
    conn = sqlite3.connect(DB_PATH, timeout=10)  # 10 сек на випадок блокування
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute(query, args)
        if commit:
            conn.commit()
            return cur.lastrowid
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv
    finally:
        conn.close()


# -------------------- USERS --------------------
@app.route('/users', methods=['GET'])
def get_users():
    users = query_db("SELECT * FROM User")
    return jsonify([dict(u) for u in users])


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = query_db("SELECT * FROM User WHERE id=?", (user_id,), one=True)
    return jsonify(dict(user)) if user else ('', 404)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    query_db(
        "INSERT INTO User (id, email, last_name, first_name, role_id) VALUES (?, ?, ?, ?, ?)",
        (data['id'], data['email'], data['last_name'], data['first_name'], data['role_id']),
        commit=True
    )
    return jsonify({'message': 'User created'}), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    query_db(
        "UPDATE User SET email=?, last_name=?, first_name=?, role_id=? WHERE id=?",
        (data['email'], data['last_name'], data['first_name'], data['role_id'], user_id),
        commit=True
    )
    return jsonify({'message': 'User updated'})


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    query_db("DELETE FROM User WHERE id=?", (user_id,), commit=True)
    return jsonify({'message': 'User deleted'})


# -------------------- QUIZZES --------------------
@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = query_db("SELECT * FROM Quiz")
    return jsonify([dict(q) for q in quizzes])


@app.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    quiz = query_db("SELECT * FROM Quiz WHERE id=?", (quiz_id,), one=True)
    return jsonify(dict(quiz)) if quiz else ('', 404)


@app.route('/quizzes', methods=['POST'])
def create_quiz():
    data = request.json
    query_db(
        "INSERT INTO Quiz (id, title, description, start_date, end_date, status, category_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (data['id'], data['title'], data['description'], data['start_date'], data['end_date'], data['status'], data['category_id']),
        commit=True
    )
    return jsonify({'message': 'Quiz created'}), 201


@app.route('/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    data = request.json
    query_db(
        "UPDATE Quiz SET title=?, description=?, start_date=?, end_date=?, status=?, category_id=? WHERE id=?",
        (data['title'], data['description'], data['start_date'], data['end_date'], data['status'], data['category_id'], quiz_id),
        commit=True
    )
    return jsonify({'message': 'Quiz updated'})


@app.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    query_db("DELETE FROM Quiz WHERE id=?", (quiz_id,), commit=True)
    return jsonify({'message': 'Quiz deleted'})


if __name__ == '__main__':
    app.run(debug=True)
