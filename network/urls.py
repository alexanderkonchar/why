from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<str:page_number>", views.page, name="index/page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:user_pk>", views.profile_view, name="profile"),
    path("following", views.following_view, name="following")
]
