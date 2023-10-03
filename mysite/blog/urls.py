from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'
"""
определяется именное пространство1
приложения с по мощью переменной app_name. Такой подход позволяет упо-
рядочивать URL-адреса по приложениям и при обращении к ним исполь-зовать имя."""
urlpatterns = [
    # представления поста
    # path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    # Шаблон URL-адреса представления post_detail принимает следующие
    # ниже аргументы:
    # • year: требуется целое число;
    # • month: требуется целое число;
    # • day: требуется целое число;
    # • post: требуется слаг (строка, содержащая только буквы, цифры, знаки
    # подчеркивания или дефисы).
    # Конвертор пути int используется для параметров year, month и day, тогда как
    # конвертор пути slug применяется для параметра post.

    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/',
         views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),

]
