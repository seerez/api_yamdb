from csv import DictReader

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comments, Genre, Genre_Title, Review,
                            Title, Users)


class Command(BaseCommand):
    help = 'Загрузка данных из csv файлов'

    def handle(self, *args, **options):
        for row in DictReader(open('static/data/category.csv')):
            category = Category(id=row['id'], name=row['name'],
                                slug=row['slug']
                                )
            category.save()

        for row in DictReader(open('static/data/comments.csv')):
            comments = Comments(id=row['id'], review_id=row['review_id'],
                                text=row['text'], author=row['author'],
                                pub_date=row['pub_date']
                                )
            comments.save()

        for row in DictReader(open('static/data/genre_title.csv')):
            genre_title = Genre_Title(id=row['id'], title_id=row['title_id'],
                                      genre_id=row['genre_id']
                                      )
            genre_title.save()

        for row in DictReader(open('static/data/genre/.csv')):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()

        for row in DictReader(open('static/data/review/.csv')):
            review = Review(id=row['id'], title_id=row['title_id'],
                            text=row['text'], author=row['author'],
                            score=row['score'], pub_date=row['pub_date']
                            )
            review.save()

        for row in DictReader(open('static/data/titles/.csv')):
            titles = Title(id=row['id'], name=row['name'],
                           year=row['year'], category=row['category']
                           )
            titles.save()

        for row in DictReader(open('static/data/users/.csv')):
            users = Users(id=row['id'], username=row['username'],
                          role=row['role'], bio=row['bio'],
                          first_name=row['first_name'],
                          last_name=row['last_name']
                          )
            users.save()
