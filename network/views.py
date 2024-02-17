from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from .models import User, Post, Follower


def index(request):
    return page(request, 1)


def page(request, page_number):
    user = request.user

    pages = Paginator(Post.objects.all().order_by("-timestamp"), 10)
    num_pages = range(1, pages.num_pages + 1)

    if request.method == "POST":
        posts = pages.page(1)
        if posts.has_next():
            next_page_number = posts.next_page_number()
        else:
            next_page_number = None
        if posts.has_previous():
            previous_page_number = posts.previous_page_number()
        else:
            previous_page_number = None

        posts = posts.object_list

        if user.is_anonymous:
            return render(request, "network/index.html", {
                "posts": posts,
                "user": user,
                "alert": "danger",
                "message": "You must be logged in to post.",
                "num_pages": num_pages,
                "next_page_number": next_page_number,
                "previous_page_number": previous_page_number
            })

        content = request.POST.get('content')
        if not content:
            return render(request, "network/index.html", {
                "posts": posts,
                "user": user,
                "alert": "danger",
                "message": "Post content cannot be empty.",
                "num_pages": num_pages,
                "next_page_number": next_page_number,
                "previous_page_number": previous_page_number
            })

        post = Post(user=user, content=content)
        post.save()

        return render(request, "network/index.html", {
            "posts": posts,
            "user": user,
            "alert": "success",
            "message": "Post added successfully!",
            "num_pages": num_pages,
            "next_page_number": next_page_number,
            "previous_page_number": previous_page_number
        })

    else:
        posts = pages.page(page_number)
        if posts.has_next():
            next_page_number = posts.next_page_number()
        else:
            next_page_number = None
        if posts.has_previous():
            previous_page_number = posts.previous_page_number()
        else:
            previous_page_number = None

        posts = posts.object_list

        try:
            return render(request, "network/index.html", {
                "posts": posts,
                "user": user,
                "num_pages": num_pages,
                "next_page_number": next_page_number,
                "previous_page_number": previous_page_number
            })
        except EmptyPage:
            return render(request, "network/error.html", {
                "error": "404 Page not found."
            }, status=404)


def profile_view(request, user_pk):
    if request.method == "POST":
        user = request.user
        profile = User.objects.get(pk=user_pk)

        if user.is_anonymous:
            return render(request, "network/error.html", {
                "error": "You must be logged in to follow a user."
            })
        elif not profile:
            return render(request, "network/error.html", {
                "error": "User to follow does not exist."
            })
        elif user.pk == profile.pk:
            return render(request, "network/error.html", {
                "error": "You can't follow yourself."
            })

        follower = Follower.objects.filter(user=user, follows=profile)

        if follower.exists():
            follower.delete()
        else:
            follower = Follower(user=user, follows=profile)
            follower.save()

        return HttpResponseRedirect(reverse("profile", args=[user_pk]))

    else:
        user = request.user
        try:
            profile = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return render(request, "network/error.html", {
                "error": "404 User not found."
            }, status=404)

        posts = Post.objects.filter(user=profile).order_by("-timestamp")

        if user.is_authenticated:
            is_follower = Follower.objects.filter(user=user, follows=profile).exists()
        else:
            is_follower = False

        follower_count = Follower.objects.filter(follows=profile).count()
        following_count = Follower.objects.filter(user=profile).count()

        return render(request, "network/profile.html", {
            "user": user,
            "profile": profile,
            "posts": posts,
            "is_follower": is_follower,
            "follower_count": follower_count,
            "following_count": following_count
        })


@login_required
def following_view(request):
    user = request.user
    people_you_follow = Follower.objects.filter(user=user).values("follows")

    posts = Post.objects.filter(user__in=people_you_follow)

    return render(request, "network/following.html", {
        "posts": posts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
