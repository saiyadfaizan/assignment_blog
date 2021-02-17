from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class User(AbstractUser):
    pass


class Post(models.Model):

    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="author"
    )
    liked = models.ManyToManyField(User, default=None, blank=True, related_name="liked")

    class Meta:
        ordering = ("-date_posted",)

    def __str__(self):
        return self.content

    @property
    def total_likes(self):
        return self.liked.all().count()


class Profile(models.Model):

    author = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name="following")
    image = models.ImageField(upload_to='image' ,null=True, blank=True)

    @property
    def total_followers(self):
        return self.following.count()

    def __str__(self):
        return str(self.author)


LIKE_CHOICES = (("Like", "Like"), ("Unlike", "Unlike"))


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default="Like", max_length=10)

    def __str__(self):
        return self.post