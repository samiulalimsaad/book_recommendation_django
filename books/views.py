from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from books.helpers import search_books
from books.models import Bookmark, History

# @login_required(login_url="login/")
# def index(req) -> HttpResponse:
#     if req.user.is_authenticated:
#         if req.method == "POST":
#             query = req.POST["query"]
#             books = search_books(query)

#             return render(
#                 req,
#                 "index.html",
#                 {"is_authenticated": req.user.is_authenticated, "books": books},
#             )
#         else:
#             user = req.user
#             return render(
#                 req,
#                 "index.html",
#                 {
#                     "is_authenticated": req.user.is_authenticated,
#                 },
#             )

#     else:
#         return render(req, "login.html", {"is_authenticated": req.user.is_authenticated})


# @login_required(login_url="login/")
def index(req) -> HttpResponse:
    if req.user.is_authenticated:
        if req.method == "POST":
            query = req.POST["query"]
            books = search_books(query)
            return render(
                req,
                "index.html",
                {
                    "is_authenticated": req.user.is_authenticated,
                    "books": books,
                    "query": query,
                },
            )
        else:
            user = req.user
            return render(
                req,
                "index.html",
                {
                    "is_authenticated": req.user.is_authenticated,
                },
            )

    else:
        return render(
            req, "login.html", {"is_authenticated": req.user.is_authenticated}
        )


def register(request) -> HttpResponse:
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(name, email, password)
        # user.has_perm('foo.add_bar')
        user.save()
        login_user(request, user)
        return redirect("index")

    return render(request, "signup.html")


def login(request) -> HttpResponse:
    if request.method == "POST":
        user = authenticate(
            request, username=request.POST["name"], password=request.POST["password"]
        )
        if user is not None:
            login_user(request, user)
            return redirect("index")
        else:
            # No backend authenticated the credentials
            ...

    return render(request, "login.html")


def logout(request) -> HttpResponse:
    logout_user(request)
    return redirect("login")


@login_required(login_url="login/")
def bookmark(req: HttpRequest, book_id) -> HttpResponse:
    user = req.user
    book = Bookmark.objects.create(user=user, book_id=book_id)
    book.save()
    return JsonResponse({"success": True})


@login_required(login_url="login/")
def details(req, book_id) -> HttpResponse:
    user = req.user
    book = History.objects.create(user=user, book_id=book_id)
    book.save()
    current_url = req.get_full_path()
    return redirect(current_url)
