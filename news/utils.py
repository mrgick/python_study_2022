from django.core.paginator import Paginator


def pagination(request, obj, max_per_page):
    """
        Добавление пагинации.
    """
    paginator = Paginator(obj, max_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
