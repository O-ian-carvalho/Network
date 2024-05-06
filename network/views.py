from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post, Likes
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(request, "network/index.html")


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


@csrf_exempt
def newpost(request):
    data = json.loads(request.body)
    agora= datetime.now()
    post = Post(content=data['content'], month=agora.month, day=agora.day, year=agora.year, hour=agora.hour, minute=agora.minute,second=agora.second, user=request.user)
    post.save()
    return JsonResponse({}, status=200)

def allposts(request):
    allposts = Post.objects.order_by( '-year', '-month','-day', '-hour', '-minute', '-second')
    array = []
    try:
        like_objects = Likes.objects.filter(user=request.user)
        for like in like_objects:
            array.append(like.post)
    except:
        array = []
    serialized_posts = []

    for post in allposts:
        likecount = 0
        try:
            like_post = Likes.objects.filter(post=post)
            likecount = len(like_post)
        except ObjectDoesNotExist:
            likecount = 0
        serialized_posts.append({'id': post.pk,'user': post.user.username,'content': post.content, 'day': post.day, 'liked': post in array, 'month': post.month, 'year': post.year, 'like_count': likecount})    
    # serialized_posts = [{'id': post.pk,'user': post.user.username,'content': post.content, 'day': post.day, 'liked': post in array, 'month': post.month, 'year': post.year} for post in allposts]
    return JsonResponse({'allposts': serialized_posts}, safe=False)

@csrf_exempt
def like(request):
    data = json.loads(request.body)
    post = Post.objects.get(pk=data['id'])

    try:
        Likes.objects.get(post=post, user=request.user).delete()
    except ObjectDoesNotExist:
        like = Likes(post=post, user=request.user)
        like.save()

    return JsonResponse({'sucess': 'sucess'},status=200)


@csrf_exempt
def profile():
    data = json.loads(request.body)