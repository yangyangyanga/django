from django.conf.urls import url

from . import views

app_name = 'comment'
urlpatterns = [
    url(r'^comments/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='comments')
]