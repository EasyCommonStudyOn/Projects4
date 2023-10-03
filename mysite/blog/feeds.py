"""
В приведенном выше исходном коде мы определили новостную ленту,
создав подкласс класса Feed фреймворка синдицированных новостных лент.
Атрибуты title, link и description соответствуют элементам RSS <title>,
<link> и <description> в указанном порядке.
Функция-утилита reverse_lazy() используется для того, чтобы генериро-
вать URL-адрес для атрибута link. Метод reverse() позволяет формировать
URL-адреса по их имени и передавать опциональные параметры
Функция-утилита reverse_lazy() представляет собой лениво вычисляемую
версию reverse(). Она позволяет использовать обратный URL-адрес до того,
как конфигурация URL-адреса проекта будет загружена.
Метод items() извлекает включаемые в новостную ленту объекты. Мы из-
влекаем последние пять опубликованных постов, которые затем будут вклю-
чены в новостную ленту.
Методы item_title(), item_description() и item_pubdate() будут получать
каждый возвращаемый методом items() объект и возвращать заголовок, опи-
сание и дату публикации по каждому элементу.
В методе item_description() используется функция markdown() , чтобы кон-
вертировать контент в формате Markdown в формат HTML, и функция шаб-
лонного фильтра truncatewords_html(), чтобы сокращать описание постов
пос ле 30 слов, избегая незакрытых HTML-тегов.
"""
import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
