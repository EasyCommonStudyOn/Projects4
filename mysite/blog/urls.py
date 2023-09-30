from django.urls import path
from . import views

app_name = 'blog'
"""
определяется именное пространство1
приложения с по мощью переменной app_name. Такой подход позволяет упо-
рядочивать URL-адреса по приложениям и при обращении к ним исполь-зовать имя."""
urlpatterns = [
    # представления поста
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail'),
]
