from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    text = models.TextField(max_length=2000, verbose_name="Описание")
    image = models.ImageField(upload_to='uploads/images',
                              blank=True,
                              verbose_name="Фотография")
    blog = models.ForeignKey(Category,
                             on_delete=models.PROTECT,
                             verbose_name='Блог')
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              verbose_name="Владелец")
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Дата создания")
    modified_date = models.DateTimeField(auto_now=True,
                                         verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def short_text(self, max_length=100):
        if len(self.text) > max_length:
            return self.text[:max_length] + "..."
        else:
            return self.text
