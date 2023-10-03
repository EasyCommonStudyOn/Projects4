from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


"""
Мы создали простой шаблонный тег, который возвращает число опубли-
кованных в блоге постов."""


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


"""
В приведенном выше исходном коде мы зарегистрировали шаблонный
тег, применяя декоратор @register.inclusion_tag. Используя blog/post/latest_
posts.html, был указан шаблон, который будет прорисовываться воз-
вращенными значениями. Шаблонный тег будет принимать опциональный
параметр count, который по умолчанию равен 5. Этот параметр позволит
задавать число отображаемых постов. Данная переменная используется для
того, чтобы ограничивать результаты запроса Post.published.order_by('-publish')[:
count].
"""


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


"""
В приведенном выше шаблонном теге с по мощью функции annotate() фор-
мируется набор запросов QuerySet, чтобы агрегировать общее число ком-
ментариев к каждому посту. Функция агрегирования Count используется для
сохранения количества комментариев в вычисляемом поле total_comments по
каждому объекту Post. Набор запросов QuerySet упорядочивается по вычис-
ляемому полю в убывающем порядке. Также предоставляется опциональная
переменная count, чтобы ограничивать общее число возвращаемых объектов."""


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
