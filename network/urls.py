from django.urls import path

from . import views
from .views import (
    index,
    login,
    logout,
    delete,
    update,
    register,
    My_Post,
    profile,
    FollowView,
    like,
    following,
    profile_detail,
    #csv_database_write,
    MailCSV,
)

urlpatterns = [
    path("index/", views.index, name="index"),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("delete/<str:pk>/", views.delete, name="delete"),
    path("update/<str:pk>/", views.update, name="update"),
    path("register/", views.register, name="register"),
    path("my_post/", My_Post.as_view(), name="my_post"),
    path("profile/", views.profile, name="profile"),
    path("follow/", views.FollowView.as_view(), name="follow"),
    path("like/", views.like, name="like"),
    path("following/", views.following, name="following"),
    path("profile_detail/<int:pk>/", views.profile_detail, name="profile_detail"),
    #path('export/csv-database-write/', views.csv_database_write, name='csv_database_write'),
    path("MailCSV/", views.MailCSV.as_view(), name="MailCSV"),
]
