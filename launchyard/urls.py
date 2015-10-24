"""launchyard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from blog.views import *

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', PublicFeedView.as_view(), name='public'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup/', CreateUserView.as_view(), name='signup'),
    url(r'^article/new/$',CreateArticleView.as_view(), name='article-new'),
    url(r'^article/edit/(?P<pk>[0-9]+)/', EditArticleView.as_view(), name='article-edit'),
    url(r'^article/delete/(?P<pk>[0-9]+)/', DeleteArticleView.as_view(), name='article-delete'),
    url(r'^public/', PublicFeedView.as_view(), name='public'),
    url(r'^home/', HomeFeedView.as_view(), name='home'),
    url(r'article/(?P<pk>[0-9]+)/','blog.views.show_article', name='show'),
]
