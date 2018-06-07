from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import markdown

from .models import Post, Category


# Create your views here.

def index(request):
    """首页"""
    post_list = Post.objects.all().order_by('-created_time')  # -号表示逆序
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    """详情页"""
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # 语法高亮扩展
        'markdown.extensions.toc',  # 自动生成目录
    ])
    return render(request, 'blog/detail.html', context={'post': post})


def archives(request, year, month):
    """归档页"""
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    """分类页"""
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def common(request):
    """评论列表"""
