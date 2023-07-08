# api_yamdb
_Учебный проект_

### Описание
>API сервис для проекта YaMDb. Проект YaMDb собирает отзывы пользователей на произведения.

### Технологии
- Python
- Django
- Django REST Framework

### Запуск проекта

Клонируйте репозиторий с сайта Github:

```sh
git clone https://github.com/beta-Lilith/api_yamdb.git
```

Установите и активируйте виртуальное окружение:

```sh
Для пользователей Windows:
python -m venv venv
source venv/Scripts/activate
```

Установите зависимости из файла requirements.txt:

```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполните миграции:

```sh
python manage.py migrate
```

Импорт данных из csv-файлов - в папке с файлом manage.py выполните команду:

```sh
python manage.py load_csv
```

Запуск проекта - в папке с файлом manage.py выполните команду:

```sh
python manage.py runserver
```

Полный список запросов и эндпоинтов описан в документации ReDoc и доступен после запуска проекта по адресу:

```sh
http://127.0.0.1:8000/redoc/
```

### Авторы

- **Ксения Оскомова** [beta-Lilith](https://github.com/beta-Lilith)
- **Павел Рванцев** [Paulman132](https://github.com/Paulman132)
- **Ирина Баронская** [Irin-Baro](https://github.com/Irin-Baro)
