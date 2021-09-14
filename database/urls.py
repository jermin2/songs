from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('song/<int:id>', views.song_view, name="song"),
    path('add', views.add, name="add"),
    path('edit/<int:id>', views.edit, name="edit")
]