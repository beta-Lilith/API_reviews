# api_yamdb
_Учебный проект_

### Описание
>API сервис для проекта YaMDb. Проект YaMDb собирает отзывы пользователей на произведения.

### Технологии
- Python
- Django
- Django REST Framework

### Запуск проекта в dev-режиме

✔Клонируйте репозиторий с сайта Github:

```sh
git clone https://github.com/beta-Lilith/api_yamdb.git
```

✔ Установите и активируйте виртуальное окружение:

```sh
Для пользователей Windows:
python -m venv venv
source venv/Scripts/activate
```

✔ Установите зависимости из файла requirements.txt:

```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

✔ Выполните миграции:

```sh
python manage.py migrate
```

✔ Импорт данных из csv-файлов - в папке с файлом manage.py выполните команду:

```sh
python manage.py load_csv
```

✔ Запуск проекта - в папке с файлом manage.py выполните команду:

```sh
python manage.py runserver
```

### Пример запроса
- GET /titles/{title_id}/reviews/

```sh
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Response samples:
```sh
200
```

Content type:
```sh
_application/json_
```

```sh
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### Авторы

| Авторы | Учебная платформа |
| ------ | ------ |
| [beta-Lilith](https://github.com/beta-Lilith), [Paulman132](https://github.com/Paulman132), [Irin-Baro](https://github.com/Irin-Baro)| [Yandex-Practicum](https://practicum.yandex.ru/backend-developer/) |
