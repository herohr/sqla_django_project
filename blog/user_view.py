from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
from blog.models import Article, User
from blog.db import Session
from django.http import HttpResponse
from django.shortcuts import render


class RegisterView(View):
    def get(self, request):
        return render(request, "user-form.html", context={"title":"注册新用户"})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            session = Session()
            ins = session.query(User).filter_by(username=username).one_or_none()
            if ins is not None:
                return HttpResponse("User already exist")

            user = User(username=username, password=password)
            session.add(user)
            session.commit()
            return redirect("/login/")
        else:
            return HttpResponse("Form")


class LoginView(View):
    def get(self, request):
        return render(request, "user-form.html", context={"title":"登录"})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            session = Session()
            ins = session.query(User).filter_by(username=username, password=password).one_or_none()

            if ins is None:
                return HttpResponse("username or password wrong")

            request.session["user_id"] = ins.id
            request.session["username"] = ins.username
            return redirect("/article-list/")

        else:
            return HttpResponse("form")
