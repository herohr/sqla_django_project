from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.views.generic import TemplateView

from blog.models import Article
from blog.db import Session
from django.shortcuts import render
from blog.md_util import md2html


class PostArticleView(View):
    def get(self, request):
        username = request.session.get("username")
        if username is None:
            return redirect("login")
        return render(request, "post-article.html")

    def post(self, request):
        username = request.session.get("username")
        if username is None:
            return redirect("login")
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.session.get("user_id")
        if title and content:
            session = Session()
            article = Article(title=title, content=md2html(content), author_id=author)
            session.add(article)
            session.commit()
            return redirect("article-list")

        else:
            return


class ArticleListView(View):
    def get(self, request):
        session = Session()
        articles = session.query(Article).order_by(Article.id.desc())
        return render(request, "article-list.html", context={"articles": articles})

    def post(self, request):
        action = request.POST.get("action")
        article_id = request.POST.get("article_id")
        user_id = request.session.get("user_id")
        if action and article_id and user_id:
            session = Session()
            article = session.query(Article).filter_by(id=article_id).one_or_none()
            if article is None:
                return HttpResponse("article not exist")
            if article.author_id != user_id:
                return HttpResponse("article is not belong to you")
            if action == "DELETE":
                session.delete(article)
                session.commit()
                return redirect("article-list")
            else:
                pass
        else:
            return redirect('article-list')


class ArticleView(View):
    def get(self, request):
        article_id = request.GET.get("id")
        session = Session()
        article = session.query(Article).filter_by(id=article_id).one_or_none()
        if article is None:
            return redirect("article-list")

        return render(request, "article.html", context={
            "title": article.title,
            "author": article.author.username,
            "create_time": article.create_time,
            "content": article.content
        })


class ArticleApiTemplateView(TemplateView):
    template_name = "article-list-api.html"
