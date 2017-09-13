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
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        '''
            在视图函数中将模板变量传递给模板是通过给render函数的context参数传递
        一个字典实现的
            例如render(request, 'blog/index.html', context={'post_list':post_list})
            这里传递了一个{'post_list':post_list}字典给模板。
            在类视图中，这个需要传递的模板变量字典是通过get_context_data获得的。
            所以覆写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        :param kwargs: 
        :return: 
        '''

        # 首先获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有paginator、page_obj、is_paginated 这三个模板变量
        # paginator 是Paginator 的一个实例
        # page_obj 是Page 的一个实例
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页10 个数据，而本身只有5 个数据，其实就用不着分页，此时is_paginated=False。
        # 由于context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意pagination_data 方法返回的也是一个字典
        context.update(pagination_data)

        # 将更新后的context返回，以便ListView使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 标示是否需要显示第一页的页码号
        # 因为如果当前页的连续页码号中含有第一页的页码号，此时就无需再显示第一的页码号，
        # 其他情况下第一页的页码是始终需要显示的。
        # 初始值为False
        first = False

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同
        last = False

        # 获得分页后的总页数
        page_range = paginator.page_range

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[](已默认为空)。
            # 此时只要获取当前右边的连续页码号
            # 比如分页页码是[1, 2, 3, 4],那么获取的就是 right = [2, 3].
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            # 切片时如果溢出自动截断
            right = page_range[page_number:page_number+2]

            # 如果最右边的页码号比最后一页的页码号减去1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其他页码，因此需要显示省略号，
            # 通过right_has_more来显示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最有边的页码号比最后一页的页码小，说明当前页右边的连续号码中
            # 不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过last来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]
            #（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码
            left = page_range[(page_number-3) if (page_number-3) > 0 else 0:page_number-1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通
            # 过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第
            # 一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码
            # 号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number-3) if (page_number-3) > 0 else 0:(page_number - 1)]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data

# class IndexView(ListView):
#     # MVT
#     model = Post    # model指定要获取的模型
#     template_name = 'blog/index.html'   # 指定视图渲染的模板
#     # Post.objects.all()
#     # 指定获取的模型列表数据保存的变量名，这个变量会被传递给模板
#     context_object_name = 'post_list' # 这个name不能瞎取，必须和模板中的值一样
#     paginate_by = 1
#
#     def pagination_data(self,paginator, page, is_paginated):
#         if not is_paginated:
#             return {}
#         # 1、first是首页
#         first = False
#         # 2、省略号
#         left_has_more = False
#         # 3、当前页左边的几个页码
#         left = []
#         # 4、当前页的页码
#         page_number = page.number
#         # 5、当前页右边的几个页码
#         right = []
#         # 6、省略号
#         right_has_more = False
#         # 7、last是最后一页
#         last = False
#
#         # 总页数
#         total_pages = paginator.num_pages
#
#         # 获取整个分页页码列表。例如共有四页时：[1,2,3,4]
#         page_range = paginator.page_range
#
#         # 如果当前页是第一页
#         if page_number == 1:
#             right = page_range[page_number:page_number+2]
#             if right[-1] < total_pages-1:
#                 right_has_more = True
#             if right[-1] < total_pages:
#                 last = True
#         # 如果当前是最后一页
#         elif page_number == total_pages:
#             left = page_range[(page_number-3) if (page_number-3) > 0 else 0:page_number]
#             if left[0] > 2:
#                 left_has_more = True
#             if left[0] > 1:
#                 first = True
#         else:
#             left = page_range[(page_number-3) if (page_number-3)>0 else 0:page_number]
#             right = page_range[page_number:page_number+2]
#             if right[-1] < total_pages - 1:
#                 right_has_more = True
#             if right[-1] < total_pages:
#                 last = True
#             if left[0]>2:
#                 left_has_more = True
#             if left[0] > 1:
#                 first = True
#         data = {
#             'left' : left,
#             'right': right,
#             'left_has_more': left_has_more,
#             'right_has_more': right_has_more,
#             'first': first,
#             'last': last,
#         }
#         return data
#
#     def get_context_data(self, **kwargs):
#         # 首先获得基类get_context_data()返回的context
#         context = super().get_context_data(**kwargs)
#         paginator = context.get('paginator')
#         page = context.get('page_obj')
#         is_paginated = context.get('is_paginated')
#
#         pagination_data = self.pagination_data(paginator, page, is_paginated)
#
#         context.update(pagination_data)
#         return context

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

    def get(self, request, *args, **kwargs):
        # 复写get方法的目的是因为每当文章被访问一次，就得将文章阅读量+1
        # get方法返回的是一个HttpResponse实例
        # 之所以需要调用父类的get方法，是因为只有当get方法被调用后，
        # 才有self.object属性，其值为Post模型实例，即被访问的文章post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量+1
        # 注意self.object的值就是被访问的文章
        self.object.increase_views()

        # 视图必须返回一个HttpResponse对象
        return response

    def get_object(self, queryset=None):
        # 覆写get_object方法的目的是因为需要对post的body值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写get_context_data的目的是因为除了将post传递给模板外（DetailView已经帮我们完成）
        # 还有把评论表单、post下的评论列表传递给模板。也就是往context里添加内容
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentsForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context

# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month,
#                                     )
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class Archives(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(
            # kwargs就是一个键值对，字典，用它代替{}
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
        )

# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # 下面中的filter(category=cate)中的category是Post中的category
        return super().get_queryset().filter(category=cate)
















