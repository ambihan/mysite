from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q
from pure_pagination import PaginationMixin
from .models import Post, Category, Tag


# Create your views here.
class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10


class PostView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'post_list'
    paginate_by = 10


class CategoryView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)


class ArchiveView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.has_toc = '<li>' in post.toc
        return post


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def search(request):
    q = request.GET.get('q')
    if not q:
        err_msg = '请输入搜索关键词'
        messages.add_message(request, messages.ERROR, err_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })
