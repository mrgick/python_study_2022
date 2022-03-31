from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import check_obj_exist, check_owner
from .models import News, Category
from .forms import NewsForm


def index(request):
    news_list = News.objects.order_by('-modified_date')[:5]
    content = {'news_list': news_list, 'title_name': 'Последние новости'}
    return render(request, 'news/newsList.html', content)


def all_blogs(request):
    blogs_list = Category.objects.all()
    content = {'blogs_list': blogs_list}
    return render(request, 'news/blogList.html', content)


@check_obj_exist(Category, 'blog_id')
def news_from_blog(request, blog_id):
    blog = Category.objects.filter(id=blog_id).first()
    news_list = News.objects.filter(blog=blog).order_by('-modified_date')
    content = {
        'news_list': news_list,
        'title_name': 'Новости блога {0}'.format(blog.name)
    }
    return render(request, 'news/newsList.html', content)


@check_obj_exist(News, 'news_id')
def news_item(request, news_id):
    news = News.objects.filter(id=news_id).first()
    content = {'news': news}
    return render(request, 'news/newsItem.html', content)


@login_required
@check_owner
@check_obj_exist(News, 'news_id')
def news_item_delete(request, news_id):
    if request.method == 'POST':
        news = News.objects.filter(id=news_id).first()
        news.delete()
        return HttpResponse({'status': 'success'})
    return render(request, '404.html')


@permission_required('is_stuff', raise_exception=True)
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
        'form': form,
        'action': '/news/add/',
        'title': 'Добавление новости'
    }
    return render(request, 'news/newsItemEditor.html', context)


@login_required
@check_owner
@check_obj_exist(News, 'news_id')
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
        'news': news,
        'form': form,
        'action': '/news/{0}/edit/'.format(news.id),
        'title': 'Редактирование новости {0}'.format(news.title)
    }
    return render(request, 'news/newsItemEditor.html', context)