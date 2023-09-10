from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("details/<str:book_id>/", views.details, name="details"),
    path("bookmark/<str:book_id>/", views.bookmark, name="bookmark"),
    # path("history/<int:book_id>/", views.todo_edit, name="history"),
    # path("favorite/<int:book_id>/", views.todo_delete, name="favorite"),
    path("signup/", views.register, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
