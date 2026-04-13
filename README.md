# VideoHub — Django Video Hosting

Платформа для загрузки и просмотра видео, написанная на Django.

## Установка и запуск

### 1. Клонируйте репозиторий
git clone https://github.com/venom8814/videohub.git
cd videohub

### 2. Создайте виртуальное окружение
# Windows
python -m venv .venv
.venv\Scripts\activate

### 3. Установите зависимости
pip install -r requirements.txt

### 4. Примените миграции
python manage.py makemigrations videos users
python manage.py migrate

### 5. Запустите сервер
python manage.py runserver

Откройте: http://127.0.0.1:8000

## Стек
- Python 3.10+ / Django 4.2 / SQLite / HTML5 + CSS3
