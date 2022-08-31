from django.core.validators import validate_slug
from django.db import models
from .validators import check_value_year_valid
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[validate_slug]
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[validate_slug]
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    description = models.TextField(null=True, blank=True)
    year = models.IntegerField(
        blank=False,
        null=False,
        validators=[check_value_year_valid],
        db_index=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

class Review(models.Model):
    # title = models.ForeignKey(
    #     'title of the production',
    #     Titles,
    #     on_delete=models.CASCADE
    # )
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.SET_NULL,
    #     related_name='rewiew',
    #     verbose_name='Автор'
    # )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Не меньше 1'),
            MaxValueValidator(10, 'Не больше 10')
        ]
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE
    )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='comments',
    #     verbose_name='Автор'
    # )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Комментарии'
