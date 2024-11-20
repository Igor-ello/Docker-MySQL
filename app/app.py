from flask import Flask, request, jsonify
import mysql.connector

# Настройки подключения к MySQL
db_config = {
    'host': 'mysql-db',  # Имя сервиса MySQL из docker-compose.yml
    'user': 'root',
    'password': 'qwerty',
    'database': 'testdb'
}

import mysql.connector

# Настройки подключения к MySQL
db_config = {
    'host': 'mysql-db',
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
    try:
        connector = mysql.connector.connect(**db_config)
        cursor = connector.cursor()

        # Запрос на создание таблицы
        create_table_query = """
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL
        );
        """

        cursor.execute(create_table_query)
        connector.commit()
        print("Таблица 'users' успешно создана.")
    except Exception as e:
        print(f"Ошибка: {str(e)}")
    finally:
        if connector.is_connected():
            cursor.close()
            connector.close()

    app.run(host='0.0.0.0', port=5000)
