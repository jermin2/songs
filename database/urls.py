from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('song/<int:id>', views.song_view, name="song"),
    path('add', views.add, name="add"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('fetch_songs', views.fetch_songs, name="fetch_songs"),
    path('book/add', views.add_book, name="add_book"),
    path('book/<int:id>', views.book_view, name="book"),
    path('books', views.books_view, name="books"),
    path('book/<int:id>/edit', views.book_edit, name="book_edit"),
    path('song_to_book', views.song_to_book, name="song_to_book"),
    path('book/<int:id>/delete', views.book_delete, name="book_delete"),
    path('favourite', views.favourite, name="favourite"),
    path('favourites', views.favourites_view, name="favourites"),
    path('sidebar', views.sidebar, name="sidebar")
]