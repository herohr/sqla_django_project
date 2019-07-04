from JsonApiView import ApiView, JsonResponse, ErrorResponse
from JsonApiView.form import JsonForm
from blog.md_util import md2html
from blog.models import *
from blog.db import Session


def user_check(request):
    username = request.json.get("username")
    password = request.json.get("password")

    session = Session()

    user = session.query(User).filter_by(username=username).one_or_none()
    session.close()
    return user


class UserApi(ApiView):
    def get(self, request):
        pass

    def post(self, request):
        print(request.json)
        form = JsonForm(request.json, ("username", "password"), username=lambda x: len(x) > 5, password=lambda x: len(x)>5)
        if not form.is_valid():
            return form.error_resp()

        session = Session()

        user = session.query(User).filter_by(username=form.username).one_or_none()
        if user is not None:
            return ErrorResponse(401, "Username already exist.")

        user = User(username=form.username, password=form.password)
        session.add(user)
        session.commit()
        return JsonResponse({})


class SessionApi(ApiView):
    def get(self, request):
        user_id = request.session.get("user_id")
        username = request.session.get("username")

        if username and user_id:
            return JsonResponse({
                "user_id": user_id,
                "username": username
            })
        else:
            return ErrorResponse(403, "User not login.")

    def post(self, request):
        username = request.json.get("username")
        password = request.json.get("password")

        session = Session()
        user = session.query(User).filter_by(username=username, password=password).one_or_none()
        if user is None:
            return ErrorResponse(401, "Username or password wrong.")

        request.session["user_id"] = user.id
        request.session["username"] = user.username

        return JsonResponse({})

    def delete(self, request):
        user_id = request.session.get("user_id")
        username = request.session.get("username")

        if user_id:
            del request.session["user_id"]
        if username:
            del request.session["username"]

        return JsonResponse({})
