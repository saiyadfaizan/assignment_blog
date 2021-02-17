from django.db import IntegrityError
from django.urls import reverse
from .models import User, Post, Profile
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm, SignUpForm, ProfileForm

from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.conf import settings
from django.core.mail import EmailMessage
import csv
import pytumblr

# from tumblr_keys import *    #this imports the content in our tumblr_keys.py file


from django.contrib.auth import get_user_model

User = get_user_model()

client = pytumblr.TumblrRestClient(
    "YarI8mnIJG3e5IfvmOkkqr0kVviLkAQv7SoWeXUHQFfhZGhQS0",
    "3sE6qJ9Tz9NRFlUGQsEGxD1TI22quLpcJpprBQWoytfCE0ZiBS",
    "g7wkKGZ9AdPUaW7dlOy6MbsE5tRjtRaYZiZFRroNZtLGeqzogP",
    "X69ZFcrjA5QpH9StmmOaHj83Hd4uyXMosX7YmLRiLyPueyJoyf",
)


@login_required()
def index(request):

    posts = Post.objects.all()
    form = PostForm()
    user = request.user

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.instance.author = request.user
            form.save()
            # import pdb; pdb.set_trace()
            client.create_text(
                "saiyadfaizan",
                state="published",
                slug="testing-text-posts",
                title="Testing",
                body=form.cleaned_data["content"],
            )

        return redirect("index")

    post_list = Post.objects.all()
    page = request.GET.get("page", 1)

    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    author = str(request.user.username)
    context = {
        "posts": posts,
        "form": form,
        "author": author,
        "post_list": post_list,
        "user": user,
    }

    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        form = AuthenticationForm()
        context = {"form": form}
        return render(request, "network/login.html", context)

    context = {"form": form}
    return render(request, "network/login.html", context)


@login_required()
def logout_view(request):
    logout(request)
    return redirect("login")


def register(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        # form1 = ProfileForm(request.POST, request.FILES)
        # Upload a profile picture from backend
        if form.is_valid():  # and form1.is_valid:
            # form1.save()
            user = form.save(request)
            Profile.objects.create(author=user)
            return redirect("login")

    else:
        form = SignUpForm()
        # form1 = ProfileForm()
    return render(request, "network/register.html", {"form": form})


@login_required()
def update(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            client.edit_post("saiyadfaizan", id=642540786226020352, type="text", title="Updated")
            form.save()
            
        return redirect("index")

    context = {"form": form}

    return render(request, "network/update.html", context)


@login_required()
def delete(request, pk):
    item = Post.objects.get(id=pk)
   
    if request.method == "POST":
         # Deletes your post :(
        item.delete()
        client.delete_post("saiyadfaizan", id=642540786226020352)
        print('deleted')
        
        return redirect("my_post")

    context = {"item": item}
    return render(request, "network/delete.html", context)


class My_Post(View, LoginRequiredMixin):
    def get(self, request):

        email = str(request.user.email)
        posts = Post.objects.filter(author__email=email)
        context = {"posts": posts}

        return render(request, "network/my_post.html", context)


@login_required()
def profile(request):

    email = str(request.user.email)
    posts = Post.objects.filter(author__email=email).order_by("date_posted")
    users = User.objects.all()
    profile = Profile.objects.all()
    context = {"posts": posts, "users": users, "profile": profile}

    return render(request, "network/profile.html", context)


@login_required()
def like(request):
    # import pdb; pdb.set_trace()
    post = get_object_or_404(Post, id=request.GET.get("post_id"))

    if post.liked.filter(id=request.user.id).exists():
        post.liked.remove(request.user)
        is_liked = False
    else:
        post.liked.add(request.user)
        is_liked = True
    data = {"is_liked": is_liked, "total_likes": post.total_likes}
    return JsonResponse(data)


class FollowView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, id=request.GET.get("profile_id"))
        following = False

        if profile.following.filter(id=request.user.id).exists():
            profile.following.remove(request.user)
            following = False
        else:
            profile.following.add(request.user)
            following = True

        data = {"following": following}
        return JsonResponse(data)


def following(request):

    profile = Profile.objects.filter(following__in=[request.user.id])
    posts = Post.objects.filter(author__profile__in=profile)
    context = {"posts": posts}
    return render(request, "network/following.html", context)


def profile_detail(request, pk):

    profile = get_object_or_404(Profile, id=pk)
    posts = Post.objects.filter(author=profile.author)
    context = {
        "posts": posts,
        "profile": profile,
    }

    return render(request, "network/profile_detail.html", context)


class MailCSV(View):
    def get(self, request):
        # queryset = Book.objects.all()
        users = User.objects.all()
        profile = Profile.objects.all()
        post = Post.objects.all()

        filename = "summary.csv"
        with open(filename, "w") as csvfile:
            cr = csv.writer(csvfile, delimiter=",", lineterminator="\n")
            cr.writerow(
                ["username", "email", "total_followers", "total_post", "total_likes"]
            )
            for user in users:
                cr.writerow(
                    [
                        user.username,
                        user.email,
                        user.profile.following.count(),
                        Post.objects.filter(author=user).count(),
                        user.liked.count(),
                    ]
                )
        csvfile.close()
        self.send_email(filename)
        return redirect("profile")

    def send_email(self, filename):
        subject = "CSV Report"
        message = "Hi, \nPlease find the attached csv."
        email = self.request.user.email

        try:
            with open(filename, "rb") as csvfile:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                mail.attach(filename, csvfile.read(), "text/csv")
                print("\nSending email..")
                mail.send()
                print("Email sent successfully!")
                return True
            csvfile.close()

        except Exception as e:
            print("Sorry mail was not sent.")
            print(e)
            return HttpResponse("Mail sent.")
