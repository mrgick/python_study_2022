from django.shortcuts import render
from .models import News
from django.db.models import Model


def check_obj_exist(model: Model, str_id: str):
    """
    Checks for obj existence. Returns 404 if failed.
    """

    def wrap(func):

        def checker(request, **kwargs):
            obj = model.objects.filter(id=kwargs[str_id]).first()
            if not obj:
                return render(request, '404.html')
            return func(request, **kwargs)

        return checker

    return wrap


def check_owner(func):
    """
    Checks if the user is the owner of the news.
    Returns 404 if failed.
    """

    def checker(request, *args, **kwargs):
        if kwargs.get('news_id'):
            news = News.objects.filter(id=kwargs['news_id']).first()
            if request.user != news.owner and not request.user.is_superuser:
                return render(request, '404.html')
        return func(request, *args, **kwargs)

    return checker