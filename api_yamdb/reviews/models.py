from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
