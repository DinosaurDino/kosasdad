from django.db import models

# Создавайте свои модели здесь.

from django.urls import reverse  # Создание URL-адресов путем изменения шаблонов URL-адресов


class Genre(models.Model):
    """Модель, представляюща жанр книг (например, научная фантастика, документальная литература)."""
    name = models.CharField(
        max_length=200,
        help_text="Введите жанр книги (например, научная фантастика, французская поэзия и т. д.)."
    )

    def __str__(self):
        """Строка для представления объекта модели (на сайте администратора и т. д.)"""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Модель, представляющая книгу (но не конкретную копию книги)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Используется внешний ключ, поскольку у книги может быть только один автор, а у авторов может быть несколько книг.
    # Автор как строка, а не как объект, потому что он еще не объявлен в файле.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # Используется ManyToManyField, потому что жанр может содержать много книг, а книга может охватывать множество жанров.
    # Класс жанра уже определен, поэтому мы можем указать объект выше.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        """Создает строку для жанра. Это необходимо для отображения жанра в Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к конкретному экземпляру книги."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта Model."""
        return self.title


import uuid  # Требуется для уникальных экземпляров книги
from datetime import date

from django.contrib.auth.models import User  # Требуется для назначения какие книги взял пользователь


class BookInstance(models.Model):
    """Модель, представляющая конкретный экземпляр книги (т. е. который можно взять в библиотеке)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        """Определяет, является ли книга просроченной, на основе даты выполнения и текущей даты."""
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'Выдана'),
        ('a', 'Доступена'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """Строка для представления объекта Model."""
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    """Модель, представляющая автора."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)


    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к конкретному экземпляру автора."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта Model."""
        return '{0}, {1}'.format(self.last_name, self.first_name)
