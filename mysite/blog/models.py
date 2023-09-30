from django.db import models
from django.utils import timezone


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)  # транслируется в столбец VARCHAR в базе дан-ных SQL
    slug = models.SlugField(max_length=250)  # короткая метка, транслируется в столбец VARCHAR в базе дан-ных SQL
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
