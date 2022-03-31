from django.shortcuts import render, redirect
from .models import News, Category
from .forms import NewsEditForm


def index(request):
    news_list = News.objects.order_by('-modified_date')[:5]
    content = {'news_list': news_list, 'title_name': 'Последние новости'}
    return render(request, 'news/newsList.html', content)


def all_blogs(request):
    blogs_list = Category.objects.all()
    content = {'blogs_list': blogs_list}
    return render(request, 'news/blogList.html', content)


def news_from_blog(request, blog_id):
    blog = Category.objects.filter(id=blog_id)
    if len(blog) == 0:
        return render(request, '404.html')
    blog = blog[0]
    news_list = News.objects.filter(blog=blog).order_by('-modified_date')
    content = {
        'news_list': news_list,
        'title_name': 'Новости блога {0}'.format(blog.name)
    }
    return render(request, 'news/newsList.html', content)


def news_item(request, news_id):
    news = News.objects.filter(id=news_id)
    if len(news) == 0:
        return render(request, '404.html')
    content = {'news': news[0]}
    return render(request, 'news/newsItem.html', content)


def news_item_edit(request, news_id):
    news = News.objects.filter(id=news_id)
    if len(news) == 0:
        return render(request, '404.html')
    elif request.user != news[0].owner:
        return render(request, '404.html')

    news = news[0]

    if request.method == 'POST':
        form = NewsEditForm(data=request.POST, files=request.FILES, instance=news)
        if form.is_valid():
            form.save()

            return redirect('/news/{0}'.format(news.id))
    else:
        form = NewsEditForm(instance=news)

    context = {'news': news, 'form': form}
    return render(request, 'news/newsItemEditor.html', context)