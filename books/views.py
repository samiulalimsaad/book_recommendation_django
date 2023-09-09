import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render


# @login_required(login_url="login/")
def index(req) -> HttpResponse:
    if req.user.is_authenticated:
        if req.method == "POST":
            query = req.POST["query"]
            res = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={query}")
            data = res.json()
            return render(
                req,
                "index.html",
                {"is_authenticated": True, "books": data["items"]},
            )
        else:
            user = req.user
            return render(
                req,
                "index.html",
                {
                    "is_authenticated": True,
                },
            )

    else:
        return render(req, "login.html", {"is_authenticated": False})


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
