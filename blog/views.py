import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag


# Create your views here.


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def archive(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year,
        created_time__month=month
    )
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(
        category=cate
    )
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(
        tag=t
    )
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ]
    )
    post.body = md.convert(post.body)
    post.toc = md.toc
    post.has_toc = '<li>' in post.toc
    return render(request, 'blog/detail.html', context={
        'post': post
    })


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def posts(request):
    post_list = Post.objects.all()
    return render(request, 'blog/posts.html', context={
        'post_list': post_list
    })
