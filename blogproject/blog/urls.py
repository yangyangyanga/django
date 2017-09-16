from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', login_required(views.PostDetailView.as_view()), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.Archives.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    # url(r'^search/$', views.search, name='search'),

    url(r'^author/$', views.get_author, name='author'),
    url(r'^publisharticle/$', views.publish_article, name='publisharticle'),
]