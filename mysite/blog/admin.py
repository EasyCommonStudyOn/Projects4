from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    """
    Теперь страница
списка содержит правую боковую панель, которая позволяет фильтровать
результаты по полям, включенным в атрибут list_filter."""
    search_fields = ['title', 'body']
    """
    На странице появилась строка поиска. Это вызвано тем, что мы опреде-
лили список полей, по которым можно выполнять поиск, используя атрибут
search_fields."""

    prepopulated_fields = {'slug': ('title',)}
    """
    Вы сообщили Django, что нужно предзаполнять поле
slug данными, вводимыми в поле title, используя атрибут prepopulated_fields:"""
    raw_id_fields = ['author']
    """
    поле author отображается поисковым виджетом, кото-
рый будет более приемлемым, чем выбор из выпадающего списка, когда у вас
тысячи пользователей. Это достигается с по мощью атрибута raw_id_fields
"""
    date_hierarchy = 'publish'
    """
    Чуть ниже строки поиска находятся навигационные ссылки
для навигации по иерархии дат; это определено атрибутом date_hierarchy."""
    ordering = ['status', 'publish']
    """
    Мы сообщаем сайту администрирования, что модель зарегистрирована на
сайте с использованием конкретно-прикладного класса, который наследует
от ModelAdmin. В этот класс можно вставлять информацию о том, как показы-
вать модель на сайте и как с ней взаимодействовать."""


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
