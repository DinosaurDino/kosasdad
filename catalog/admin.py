from django.contrib import admin

# Зарегистрируйте свои модели здесь..

from .models import Author, Genre, Book, BookInstance, Language

"""Ну по факту они тут не нужны))
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookInstance)
"""

admin.site.register(Genre)
admin.site.register(Language)


class BooksInline(admin.TabularInline):
    """Определяет формат встроенной вставки книги (используется в AuthorAdmin)"""
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Объект администрирования для моделей Author.
    Определяет:
     - поля для отображения в виде списка (list_display)
     - поля заказов в подробном виде (поля),
       группировка полей даты по горизонтали
     - добавляет встроенное добавление книг в авторском представлении (inlines)
    """
    list_display = ('last_name',
                    'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]


class BooksInstanceInline(admin.TabularInline):
    """Определяет формат встроенной вставки экземпляра книги (используется в BookAdmin)"""
    model = BookInstance


class BookAdmin(admin.ModelAdmin):
    """Объект администрирования для моделей Book.
    Определяет:
     - поля для отображения в виде списка (list_display)
     - добавляет встроенное добавление экземпляров книги в книжном представлении (встроенные)
    """
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


admin.site.register(Book, BookAdmin)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """Объект администрирования для моделей BookInstance.
    Определяет:
     - поля для отображения в виде списка (list_display)
     - фильтры, которые будут отображаться на боковой панели (list_filter)
     - группировка полей в секции (fieldsets)
    """
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
