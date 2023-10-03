from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    """
   Представление принимает опциональный параметр tag_slug, значение
которого по умолчанию равно None. Этот параметр будет передан в URL-
адресе.
2. Внутри указанного представления формируется изначальный набор
запросов, извлекающий все опубликованные посты, и если имеется
слаг данного тега, то берется объект Tag с данным слагом, используя
функцию сокращенного доступа get_object_or_404().
3. Затем список постов фильтруется по постам, которые содержат дан-
ный тег. Поскольку здесь используется взаимосвязь многие-ко-многим,
необходимо фильтровать записи по тегам, содержащимся в заданном
списке, который в данном случае содержит только один элемент. Здесь
используется операция __in поиска по полю. Взаимосвязи многие-ко-
многим возникают, когда несколько объектов модели ассоциированы
с несколькими объектами другой модели. В нашем приложении пост
может иметь несколько тегов, и тег может быть связан с несколькими
постами. 
    """
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    # posts = paginator.page(page_number)  # Мы создаем экземпляр класса Paginator с числом объектов, возвраща-
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

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})


# Если page_number находится вне диапазона, то
# выдать последнюю страницу


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментирования пользователями
    form = CommentForm()
    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]
    """
    Приведенный выше исходный код делает следующее:
1) извлекается Python’овский список идентификаторов тегов текущего
поста. Набор запросов QuerySet values_list() возвращает кортежи со
значениями заданных полей. Ему передается параметр flat=True, чтобы
получить одиночные значения, такие как [1, 2, 3, ...], а не одноэле-
ментые кортежи, такие как [(1,), (2,), (3,) ...];
2) берутся все посты, содержащие любой из этих тегов, за исключением
текущего поста;
3) применяется функция агрегирования Count. Ее работа – генерировать
вычисляемое поле – same_tags, – которое содержит число тегов, общих
со всеми запрошенными тегами;
4) результат упорядочивается по числу общих тегов (в убывающем по-
рядке) и по publish, чтобы сначала отображать последние посты для
постов с одинаковым числом общих тегов. Результат нарезается, чтобы
получить только первые четыре поста;
5) объект similar_posts передается в контекстный словарь для функции
render()."""
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts
                   })


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


"""
атрибут queryset используется для того, чтобы иметь конкретно-при-
кладной набор запросов QuerySet, не извлекая все объекты. Вместо
определения атрибута queryset мы могли бы указать model=Post, и Django
сформировал бы для нас типовой набор запросов Post.objects.all();
• контекстная переменная posts используется для результатов запроса.
Если не указано имя контекстного объекта context_object_name, то по
умолчанию используется переменная object_list;
• в атрибуте paginate_by задается постраничная разбивка результатов
с возвратом трех объектов на страницу;
• конкретно-прикладной шаблон используется для прорисовки страницы
шаблоном template_name. Если шаблон не задан, то по умолчанию List-
View будет использовать blog/post_list.html."""


def post_share(request, post_id):
    # Извлечь пост по его идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


"""
Мы определили представление post_share, которое в качестве параметров
принимает объект request и переменную post_id. Мы используем функцию
сокращенного доступа get_object_or_404(), чтобы извлечь опубликованный
пост по его id.
Одно и то же представление используется как для отображения изначаль-
ной формы на странице, так и для обработки представленных для валида-
ции данных. HTTP-метод request позволяет различать случаи, когда форма
передается на обработку. Запрос GET будет указывать на то, что пользователю
должна быть отображена пустая форма, а запрос POST – на то, что форма пере-
дается на обработку. Булево выражение request.method == 'POST' используется
для того, чтобы прово дить различие ме жду э тими двумя сценариями.
"""


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request,
                  'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


"""
По id поста извлекается опубликованный пост, используя функцию со-
кращенного доступа get_object_or_404().
2. Определяется переменная comment с изначальным значением None. Ука-
занная переменная будет использоваться для хранения комментарного
объекта при его создании.
3. Создается экземпляр формы, используя переданные на обработку POST-
данные, и проводится их валидация методом is_valid(). Если форма
невалидна, то шаблон прорисовывается с ошибками валидации.
4. Если форма валидна, то создается новый объект Comment, вызывая ме-
тод save() формы, и назначается переменной new_comment, как показано
ниже:
comment = form.save(commit=False)
5. Метод save() создает экземпляр модели, к которой форма привязана,
и сохраняет его в базе данных. Если вызывать его, используя commit=False,
то экземпляр модели создается, но не сохраняется в базе данных. Такой
подход позволяет видоизменять объект перед его окончательным со-
хранением.
6. Пост назначается созданному комментарию:
comment.post = post
7. Новый комментарий создается в базе данных путем вызова его метода
save():
comment.save()
8. Прорисовывается шаблон blog/post/comment.html, передавая объекты
post, form и comment в контекст шаблона. Этот шаблон еще не существует;
мы создадим его позже.
"""


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + \
                            SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


"""
В приведенном выше представлении сначала создается экземпляр формы
SearchForm. Для проверки того, что форма была передана на обработку, в сло-
варе request.GET отыскивается параметр query. Форма отправляется методом
GET, а не методом POST, чтобы результирующий URL-адрес содержал пара-
метр query и им было легко делиться. После передачи формы на обработку
создается ее экземпляр, используя переданные данные GET, и проверяется
валидность данных формы. Если форма валидна, то с по мощью конкретно-
прикладного экземпляра SearchVector, сформированного с использованием
полей title и body, выполняется поиск опубликованных постов. В приведенном выше исходном коде к векторам поиска, сформированным
с использованием полей title и body, применяются разные веса. По умолча-
нию веса таковы: D, C, B и A, и они относятся соответственно к числам 0.1, 0.2,
0.4 и 1.0. Вес 1.0 применяется к вектору поиска title (A), и вес 0.4 – к вектору
body (B). Совпадения с заголовком будут преобладать над совпадениями с со-
держимым тела поста. Результаты фильтруются, чтобы отображать только те,
у которых ранг выше 0.3."""
