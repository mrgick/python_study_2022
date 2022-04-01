from django.shortcuts import render
from .models import News
from django.db.models import Model


def check_obj_exist(model: Model, str_id: str):
    """
    Decorator for views that checks for obj existence.
    Returns 404 if failed.
    """

    def wrap(func):

        def checker(request, **kwargs):
            obj = model.objects.filter(id=kwargs[str_id]).first()
            if not obj:
                return render(request, '404.html', status=404)
            return func(request, **kwargs)

        return checker

    return wrap


def check_owner(func):
    """
    Decorator for views that checks if the user is the owner of the news.
    Returns 403 if failed.
    """

    def checker(request, *args, **kwargs):
        if kwargs.get('news_id'):
            news = News.objects.filter(id=kwargs['news_id']).first()
            if request.user != news.owner and not request.user.is_superuser:
                return render(request, '403.html', status=403)
        return func(request, *args, **kwargs)

    return checker
