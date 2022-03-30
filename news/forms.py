from email.policy import default
from tkinter.ttk import Widget
from django import forms
from .models import News, Category


class CategoryChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "Категория: {}".format(obj.name)


class NewsEditForm(forms.ModelForm):

    blog = CategoryChoiceField(queryset=Category.objects.all(), label=News._meta.get_field('blog').verbose_name)

    class Meta:
        model = News
        fields = ('title', 'text', 'image', 'blog')
    