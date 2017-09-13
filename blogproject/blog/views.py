from django.shortcuts import render, get_object_or_404
from .models import Post, Category
import markdown
from django.views.generic import ListView,DetailView

from comment.forms import CommentsForm

# Create your views here.
# def index(request):
#     # return HttpResponse("<h1>yang is happy</h1>")
#     post1 = Post.objects.all()
#     context = {
#         'title': "yang & blog",
#         'post_list': post1,
#     }
#     return render(request, "blog/index.html", context)

class IndexView(ListView):
    # MVT
    model = Post    # model指定要获取的模型
    template_name = 'blog/index.html'   # 指定视图渲染的模板
    # Post.objects.all()
    # 指定获取的模型列表数据保存的变量名，这个变量会被传递给模板
    context_object_name = 'post_list' # 这个name不能瞎取，必须和模板中的值一样


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.increase_views()
#     # category = post.category.name
#     post.body = markdown.markdown(post.body,
#                     extensions=[
#                         'markdown.extensions.extra',
#                         'markdown.extensions.codehilite',
#                         'markdown.extensions.toc'
#                     ])
#     form = CommentsForm()
#     comment_list = post.comment_set.all()
#
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list}
#     return render(request, 'blog/detail.html', context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        # 获得post对象
        post = super().get_object(queryset)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return post

    def get_context_data(self, **kwargs):
        # 把post加到context
        context = super().get_context_data(**kwargs)
        form = CommentsForm()
        comment_list = self.object.comment_set.all()
        context.update({    # context已有post了，所以这里使用更新update
            'form': form,
            'comment_list': comment_list,
        })
        return context

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})

class Archives(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(
            # kwargs就是一个键值对，字典，用它代替{}
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
        )

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # 下面中的filter(category=cate)中的category是Post中的category
        return super().get_queryset().filter(category=cate)
















