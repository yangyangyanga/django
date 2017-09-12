#一级标题
## 二级标题
###三级标题

- djas
- a
- b
- c

1.dd
2.ss
3.ww

>sada

[百度](www.baidu.com)

![tupian]()

*baidu*
**baidu**

```python
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # category = post.category.name
    post.body = markdown.markdown(post.body,
                    extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc'
                    ])
    context = {'post': post}
    return render(request, 'blog/detail.html', context)
```
