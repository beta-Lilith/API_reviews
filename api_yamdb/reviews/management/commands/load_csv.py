import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import (Category, Comment, Review,
                       Genre, GenreTitle,
                       Title, User)

DATA = [
    (User, 'users.csv'),
    (Category, 'category.csv'),
    (Genre, 'genre.csv'),
    (Title, 'titles.csv'),
    (GenreTitle, 'genre_title.csv'),
    (Review, 'review.csv'),
    (Comment, 'comments.csv'),
]

ERROR_MESSAGE = ('Ошибка при загрузке данных'
                 'для модели "{model_name}": {error}')

SUCCESS_MESSAGE = 'Данные для модели "{model_name}" успешно загружены'


class Command(BaseCommand):
    """Импорт данных из csv-файлов"""
    help = ('Чтобы запустить импорт данных из csv-файлов, '
            'выполните команду "python manage.py load_csv".')

    def handle(self, *args, **options):
        for model, filename in DATA:
            file = os.path.join(settings.STATICFILES_DIRS[0], 'data', filename)
            with open(file, encoding='utf-8') as csv_file:
                file_reader = csv.DictReader(csv_file)
                for data in file_reader:
                    try:
                        if model == Title and 'category' in data:
                            data['category'] = Category.objects.get(
                                id=data.pop('category'))
                        if model in (Review, Comment) and 'author' in data:
                            data['author'] = User.objects.get(
                                id=data.pop('author'))
                        model.objects.get_or_create(**data)
                    except ValueError as error:
                        self.stdout.write(self.style.ERROR(
                            ERROR_MESSAGE.format(model_name=model.__name__,
                                                 error=error)))
                self.stdout.write(self.style.SUCCESS(
                    SUCCESS_MESSAGE.format(model_name=model.__name__)))
