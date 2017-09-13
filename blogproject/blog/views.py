from django.shortcuts import render, get_object_or_404
from .models import Post, Category
import markdown
from django.views.generic import ListView

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
    model = Post    # model指定模型类名
    template_name = 'blog/index.html'   # 指定视图渲染的模板
    # Post.objects.all()
    context_object_name = 'post_list' # 这个name不能瞎取，必须和模板中的值一样


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    # category = post.category.name
    post.body = markdown.markdown(post.body,
                    extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc'
                    ])
    form = CommentsForm()
    comment_list = post.comment_set.all()

    context = {'post': post,
               'form': form,
               'comment_list': comment_list}
    return render(request, 'blog/detail.html', context)

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})

















