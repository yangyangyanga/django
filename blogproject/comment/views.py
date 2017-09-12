from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post

from .models import Comment
from .forms import CommentsForm

def post_comment(request,post_pk):
    # 获得要评论的文章
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentsForm(request.POST)   # 实例化表单对象
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存
            # 评论数据到数据库。因为还要和被评论文章关联起来
            comment = form.save(commit=False)   # 由表单对象得到模型对象
            comment.post = post
            comment.save()
            # 可以直接重定向到Post模型当中
            # 因为指定了get_absolute_url
            return redirect(post)
        else:
            # 获取文章已有的评论
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list,
            }
            return render(request, 'blog/detail.html',context=context)
    return redirect(post)