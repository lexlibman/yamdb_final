import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class RoleChoices(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class MyUser(AbstractUser):

    email = models.EmailField('Адрес эл.почты', unique=True)
    bio = models.CharField(
        'О себе',
        max_length=150,
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=100,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=64,
        blank=True
    )

    class Meta:
        ordering = ('username', )

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == RoleChoices.MODERATOR or self.is_staff

    @property
    def is_administrator(self):
        return self.role == RoleChoices.ADMIN or self.is_superuser


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя жанра',
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
        unique=True
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        null=True,
        blank=True,
        validators=(MaxValueValidator(datetime.date.today().year),),
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        blank=True,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Review (models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        help_text='Произведение к котрому написан отзыв',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        MyUser,
        verbose_name='Автор',
        help_text='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=False,
        null=False
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Пишите любой текст, но не оставляйте поле пустым.',
        blank=False,
        null=False
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        help_text='Поставьте оценку произведению, от 1 до 10',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        blank=False,
        null=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        unique_together = ['author', 'title']

    def __str__(self):
        output_text = self.show_text_preview()
        author = self.author

        return f'Author: {author}, Date: {self.pub_date:%Y-%m-%d}, Text: {output_text}'
    __str__.short_description = 'Review preview'
    post_preview = property(__str__)

    def show_text_preview(self):
        if not self.text:
            return '-пусто-'
        if len(self.text) < 200:
            return self.text

        return self.text[0:180] + '...'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        help_text='Отзыв к которому написан комментарий',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        MyUser,
        verbose_name='Автор',
        help_text='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=False,
        null=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
        blank=False,
        null=False
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Пишите любой текст, но не оставляйте поле пустым.',
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['-pub_date']

    def __str__(self):
        output_text = self.show_text_preview()
        author = self.author

        return f'Author: {author}, Date: {self.pub_date:%Y-%m-%d}, Text: {output_text}'
    __str__.short_description = 'Comment preview'
    post_preview = property(__str__)

    def show_text_preview(self):
        if not self.text:
            return '-пусто-'
        if len(self.text) < 200:
            return self.text

        return self.text[0:180] + '...'
