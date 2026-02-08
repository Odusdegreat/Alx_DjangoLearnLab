from django.urls import path
from .views import AuthorListCreateView, BookListCreateView

urlpatterns = [
    path("authors/", AuthorListCreateView.as_view(), name="authors-list-create"),
    path("books/", BookListCreateView.as_view(), name="books-list-create"),
]
