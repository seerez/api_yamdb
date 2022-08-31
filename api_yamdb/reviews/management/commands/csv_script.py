from django.core.management.base import BaseCommand
from reviews.models import (Rewiew, Comments, Category, Genre_Title,
                            Genre, Titles, Users
                            )
from csv import DictReader


class Command(BaseCommand):
    help = 'Загрузка данных из csv файлов'

    def handle(self, *args, **options):
        for row in DictReader(open('static/date/category.csv')):
            category = Category(id=row['id'], name=row['name'],
                                slug=row['slug']
                                )
            category.save()

        for row in DictReader(open('static/date/comments.csv')):
            comments = Comments(id=row['id'], review_id=row['review_id'],
                                text=row['text'], author=row['author'],
                                pub_date=row['pub_date']
                                )
            comments.save()

        for row in DictReader(open('static/date/genre_title.csv')):
            genre_title = Genre_Title(id=row['id'], title_id=row['title_id'],
                                      genre_id=row['genre_id']
                                      )
            genre_title.save()

        for row in DictReader(open('static/date/genre/.csv')):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()

        for row in DictReader(open('static/date/review/.csv')):
            rewiew = Rewiew(id=row['id'], title_id=row['title_id'],
                            text=row['text'], author=row['author'],
                            score=row['score'], pub_date=row['pub_date']
                            )
            rewiew.save()

        for row in DictReader(open('static/date/titles/.csv')):
            titles = Titles(id=row['id'], name=row['name'],
                            year=row['year'], category=row['category']
                            )
            titles.save()

        for row in DictReader(open('static/date/users/.csv')):
            users = Users(id=row['id'], username=row['username'],
                          role=row['role'], bio=row['bio'],
                          first_name=row['first_name'],
                          last_name=row['last_name']
                          )
            users.save()
