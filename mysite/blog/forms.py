# Django поставляется с двумя базовыми классами для разработки форм:
# • Form: позволяет компоновать стандартные формы путем определения
# полей и валидаций;
# • ModelForm: позволяет компоновать формы, привязанные к экземплярам
# модели. Он предоставляет все функциональности базового класса Form,
# но поля формы можно объявлять явным образом или автоматически
# генерировать из полей модели. Форму можно использовать для созда-
# ния либо редактирования экземпляров модели.

from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Для того чтобы создать форму из модели, надо в Meta-классе формы просто указать модель, для которой следует компоновать форму.
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()
