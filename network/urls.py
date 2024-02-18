from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<str:page_number>", views.index_pagination, name="index/page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:user_pk>", views.profile_view, name="profile"),
    path("user/<str:user_pk>/page/<str:page_number>", views.profile_view_pagination, name="profile/page"),
    path("following", views.following_view, name="following")
]
