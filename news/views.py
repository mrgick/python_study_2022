from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .decorators import check_obj_exist, check_owner
from .models import News, Category
from .forms import NewsForm, CategoryForm
from .utils import pagination


def home(request):
    news_list = News.objects.order_by('-modified_date')[:5]
    page_obj = pagination(request, news_list, 10)
    content = {'page_obj': page_obj, 'title_name': 'Последние новости'}
    return render(request, 'news/newsList.html', content)


def all_blogs(request):
    blogs_list = Category.objects.all().order_by('name')
    page_obj = pagination(request, blogs_list, 10)
    content = {'page_obj': page_obj}
    return render(request, 'news/blogList.html', content)


@permission_required('news.add_category', raise_exception=True)
@staff_member_required
def blog_item_add(request):
    print(request.user)
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            blog_name = form.cleaned_data.get('name')
            blog = Category.objects.filter(name=blog_name)
            if not blog:
                blog = form.save()
                msg = "Блог {0}:{1} добавлен.".format(blog.id, blog.name)
                context = {'msg': msg, 'no_redirect': True}
                return render(request, 'info.html', context)
            form.add_error('name',
                           "Блог {0} уже существует.".format(blog_name))
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'news/blogAddItem.html', context)


@check_obj_exist(Category, 'blog_id')
def news_from_blog(request, blog_id):
    blog = Category.objects.filter(id=blog_id).first()
    news_list = News.objects.filter(blog=blog).order_by('-modified_date')
    page_obj = pagination(request, news_list, 10)
    content = {
        'page_obj': page_obj,
        'title_name': 'Новости блога {0}'.format(blog.name)
    }
    return render(request, 'news/newsList.html', content)


@check_obj_exist(News, 'news_id')
def news_item(request, news_id):
    news = News.objects.filter(id=news_id).first()
    content = {'news': news}
    return render(request, 'news/newsItem.html', content)


@check_obj_exist(News, 'news_id')
@permission_required('news.delete_news', raise_exception=True)
@staff_member_required
@check_owner
def news_item_delete(request, news_id):
    if request.method == 'POST':
        news = News.objects.filter(id=news_id).first()
        news.delete()
        return redirect('/blog/{0}/'.format(news.blog.id))
    return render(request, '404.html')


@permission_required('news.add_news', raise_exception=True)
@staff_member_required
def news_item_add(request):
    if request.method == 'POST':
        news = News(owner=request.user)
        form = NewsForm(data=request.POST, files=request.FILES, instance=news)
        if form.is_valid():
            news = form.save()
            return redirect('/news/{0}'.format(news.id))
    else:
        form = NewsForm()

    context = {
        'action': 'add',
        'form': form,
        'url': '/news/add/',
        'title': 'Добавление новости'
    }
    return render(request, 'news/newsItemEditor.html', context)


@check_obj_exist(News, 'news_id')
@permission_required('news.change_news', raise_exception=True)
@staff_member_required
@check_owner
def news_item_edit(request, news_id):
    news = News.objects.filter(id=news_id).first()

    if request.method == 'POST':
        form = NewsForm(data=request.POST, files=request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('/news/{0}'.format(news.id))
    else:
        form = NewsForm(instance=news)

    context = {
        'action': 'edit',
        'news': news,
        'form': form,
        'url': '/news/{0}/edit/'.format(news.id),
        'title': 'Редактирование новости {0}'.format(news.title)
    }
    return render(request, 'news/newsItemEditor.html', context)
