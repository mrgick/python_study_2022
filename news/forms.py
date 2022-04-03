from django import forms
from .models import News, Category


class CategoryChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "Категория: {}".format(obj.name)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)


class NewsForm(forms.ModelForm):

    blog = CategoryChoiceField(queryset=Category.objects.all(),
                               label=News._meta.get_field('blog').verbose_name)

    class Meta:
        model = News
        fields = ('title', 'text', 'image', 'blog')
