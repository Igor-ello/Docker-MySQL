from typing import Optional

from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector.abstracts import MySQLCursorAbstract, MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

# Настройки подключения к MySQL
db_config = {
    'host': 'mysql-db',  # Имя сервиса MySQL из docker-compose.yml
    'user': 'root',
    'password': 'qwerty',
    'database': 'testdb'
}

app = Flask(__name__)

# Роут для проверки работы приложения
@app.route('/')
def home():
    return "Flask приложение работает!"


# Роут для добавления данных в базу
@app.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({"error": "Имя и возраст обязательны"}), 400

    try:
        connector = mysql.connector.connect(**db_config)
        cursor = connector.cursor()
        query = "INSERT INTO users (name, age) VALUES (%s, %s)"
        cursor.execute(query, (name, age))
        connector.commit()
        return jsonify({"message": "Пользователь добавлен"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Роут для получения данных из базы
@app.route('/users', methods=['GET'])
def get_users():

    try:
        connector = mysql.connector.connect(**db_config)
        cursor = connector.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
