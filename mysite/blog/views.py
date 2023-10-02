from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number) #Мы создаем экземпляр класса Paginator с числом объектов, возвраща-
# емых в расчете на страницу. Мы будем отображать по три поста на
# страницу.
# 2. Мы извлекаем HTTP GET-параметр page и сохраняем его в переменной
# page_number. Этот параметр содержит запрошенный номер страницы.
# Если параметра page нет в GET-параметрах запроса, то мы используем
# стандартное значение 1, чтобы загрузить первую страницу результатов.
# 3. Мы получаем объекты для желаемой страницы, вызывая метод page()
# класса Paginator. Этот метод возвращает объект Page, который хранится
# в переменной posts.
# 4. Мы передаем номер страницы и объект posts в шаблон.
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
