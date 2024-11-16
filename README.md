# Структура проекта

```commandline
docker_mysql/
├── app/
│   ├── app.py             # Основное приложение Flask
│   ├── requirements.txt   # Список зависимостей Python
├── docker-compose.yml     # Docker Compose для запуска сервисов
├── Dockerfile             # Dockerfile для Flask-приложения
```

---

# Взаимодействие

Добавление пользователя:
```
curl -X POST -H "Content-Type: application/json" -d '{"name": "Alice", "age": 25}' http://localhost:5000/add
```

Получение пользователей:
```
curl http://localhost:5000/users
```

Подключение к базе данных:
```
docker exec -it mysql-db mysql -u root -p
```

Проверьте содержимое базы testdb и таблицы users:
```
SELECT * FROM users;
```