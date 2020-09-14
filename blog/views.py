from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    #  Вместо задания атрибута QuerySet мы могли бы указать модель model=Post,
    #  и тогда Django, используя стандартный менеджер модели, получал бы объекты как Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    #  Базовый обработчик Django ListView передает объект в качестве переменной с именем page_obj


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})
    # Вообще, при удалении из словаря "page", в работе блога ничего не меняется (на этапе создания пагинатора)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day
    )
    return render(request, 'blog/post/detail.html', {'post': post})
