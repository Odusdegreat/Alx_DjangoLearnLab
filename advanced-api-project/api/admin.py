from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_of_birth']
    search_fields = ['name']
    list_filter = ['date_of_birth']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'isbn', 'published_date', 'price']
    search_fields = ['title', 'isbn', 'author__name']
    list_filter = ['published_date', 'author']
    raw_id_fields = ['author']