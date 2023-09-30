"""
1.Каждая модель Django
имеет по меньшей мере один модельный менеджер, а менеджер, который
применяется по умолчанию, называется objects. Набор запросов QuerySet
можно получать с по мощью модельного менеджера.

2.Запросы с операциями поиска в полях формируются с использованием двух
знаков подчеркивания, например publish__year, но те же обозначения также
используются для обращения к полям ассоциированных моделей, например
author__username.

3.Определенные результаты можно исключать из набора запросов QuerySet,
используя метод exclude() менеджера.

4.Используя метод order_by() менеджера, можно упорядочивать результаты по
разным полям.

5.Если необходимо удалить объект, то это можно сделать из экземпляра объ-
екта, используя метод delete()

6.Если менеджер
в модели не определен, то Django автоматически создает для нее стандарт-
ный менеджер objects.
7.
8.
9.
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)
"""
Есть два способа добавлять или адаптировать модельные менеджеры под
конкретно-прикладную задачу: можно добавлять дополнительные методы
менеджера в существующий менеджер либо создавать новый менеджер, ви-
доизменив изначальный набор запросов QuerySet, возвращаемый менедже-
ром."""

class Post(models.Model):
    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)  # транслируется в столбец VARCHAR в базе дан-ных SQL
    slug = models.SlugField(max_length=250)  # короткая метка, транслируется в столбец VARCHAR в базе дан-ных SQL
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    # Это поле определяет взаимосвязь многие-
    # к-одному, означающую, что каждый пост написан пользователем и пользо-
    # ватель может написать любое число постов. Для этого поля Django создаст
    # внешний ключ в базе данных, используя первичный ключ соответствующей
    # модели.
    body = models.TextField()  # транслируется в столбец Text в базе данных SQL.
    publish = models.DateTimeField(default=timezone.now)  # транслируется в столбец DATETIME в базе данных SQL
    created = models.DateTimeField(auto_now_add=True)  # дата будет сохраняться автоматически во время создания объекта;
    updated = models.DateTimeField(auto_now=True)  # дата будет обновляться автоматически во время сохранения объекта.
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              #                             параметр choices, чтобы ограничивать
                              # значение поля вариантами из Status.choices. Кроме того, применяя параметр
                              # default, задано значение поля, которое будет использоваться по умолчанию.
                              # В этом поле статус DRAFT используется в качестве предустановленного вари-
                              # анта, если не указан иной.
                              default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']  # сортировать результаты по полю publish
        indexes = [
            # позволяет определять в модели индексы базы данных, которые могут содержать одно или несколько полей в возрастающем либо убывающем порядке
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    # Django будет использовать этот метод
    # для отображения имени объекта во многих местах, таких как его сайт адми-
    # нистрирования.
