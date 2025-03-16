# Онлайн-платформа для бронювання та управління послугами приватних майстрів 🎈

## 🚀 Встановлення та запуск проекту

### 📌 1. Клонування репозиторію
```sh
git clone https://github.com/yourusername/barber-booking.git
cd barber-booking
```

### 📌 2. Створення та активація віртуального середовища
#### Для Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

#### Для macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

### 📌 3. Застосування міграцій бази даних
```sh
python manage.py migrate
```

### 📌 4. Створення суперкористувача (опційно)
```sh
python manage.py createsuperuser
```

### 📌 5. Запуск локального сервера
```sh
python manage.py runserver
```

📅 **Проект буде доступний за адресою:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 🛠 Використані технології
- **Django** — Web-фреймворк для бекенду
- **SQLite** — База даних за замовчуванням
- **HTML, CSS** — Фронтенд
- **Bootstrap** — UI-стилі
- **JavaScript** — Клієнтська логіка
