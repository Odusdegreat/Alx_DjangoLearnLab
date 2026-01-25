from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # ------------------------
    # Book permission-based views
    # ------------------------
    path("add_book/", views.add_book_view, name="add_book"),       # literally "add_book/"
    path("edit_book/", views.change_book_view, name="edit_book"),  # literally "edit_book/"
    path("delete_book/", views.delete_book_view, name="delete_book"), # literally "delete_book/"

    # ------------------------
    # Auth views
    # ------------------------
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # ------------------------
    # Books and Library
    # ------------------------
    path("", views.list_books, name="list_books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
    
    # ------------------------
    # Role-based views
    # ------------------------
    path("admin_dashboard/", views.admin_view, name="admin_dashboard"),
    path("librarian_dashboard/", views.librarian_view, name="librarian_dashboard"),
    path("member_dashboard/", views.member_view, name="member_dashboard"),
]
