"""sqla_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import *
from blog.user_view import *
from blog.article_api import *
from blog.user_api import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view()),
    path('', lambda r: redirect("article-list")),
    path('article/', ArticleView.as_view()),
    path("post-article/", PostArticleView.as_view(),),
    path("article-list/", ArticleApiTemplateView.as_view(), name="article-list"),
]


def api(url, api_view):
    return path("api/"+url, api_view)


apis = [
    api("article/", ArticleApi.as_view()),
    api("user/", UserApi.as_view()),
    api("session/", SessionApi.as_view())
]

urlpatterns.extend(apis)
