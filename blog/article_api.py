from JsonApiView import ApiView, JsonResponse, ErrorResponse
from JsonApiView.form import JsonForm
from blog.md_util import md2html
from blog.models import *
from blog.db import Session


class ArticleApi(ApiView):
    def get(self, request):
        article_id = request.GET.get("article_id")
        session = Session()
        if article_id is None:
            articles = session.query(Article).order_by(Article.id.desc()).all()
            rs = []
            for i in articles:
                _dict = i.serialize()
                _dict["author_name"] = i.author.username
                rs.append(_dict)

            return JsonResponse({"articles": rs})

        article = get_by_pk(session, Article, article_id)
        if article is None:
            return ErrorResponse(404, "Article not found")
        rsp = article.serialize()
        rsp["author_name"] = article.author.username
        return JsonResponse(rsp)

    def post(self, request):
        user_id = request.session.get("user_id")
        if user_id is None:
            return ErrorResponse(401, "Login first")

        form = JsonForm(request.json, ("title", "content"))
        if not form.is_valid():
            return form.error_resp()

        title = form.title
        content = form.content
        author_id = user_id
        article = Article(title=title, content=md2html(content), author_id=author_id)

        session = Session()
        session.add(article)
        session.commit()

        return JsonResponse({})

    def put(self, request):
        user_id = request.session.get("user_id")
        if user_id is None:
            return ErrorResponse(401, "Login first")

        form = JsonForm(request.json, ("id", "title", "content"))
        if not form.is_valid():
            return form.error_resp()

        title = form.title
        content = form.content
        session = Session()
        article = get_by_pk(session, Article, form.id)
        if article is None:
            return ErrorResponse(404, "Article not found.")
        if article.author_id != user_id:
            return ErrorResponse(403, "The article is not belong to you.")

        session.add(article)
        article.title, article.content = title, content
        session.commit()

        return JsonResponse({})

    def delete(self, request):
        user_id = request.session.get("user_id")
        if user_id is None:
            return ErrorResponse(401, "Login first")

        form = JsonForm(request.json, ("article_id", ))
        if not form.is_valid():
            return form.error_resp()
        session = Session()
        article = get_by_pk(session, Article, form.article_id)
        if article is None:
            return ErrorResponse(404, "Article not found.")
        if article.author_id != user_id:
            return ErrorResponse(403, "The article is not belong to you.")

        session.delete(article)
        session.commit()
        return JsonResponse({})
