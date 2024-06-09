from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User

User = get_user_model()


class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    last_name = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    age = models.IntegerField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class CustomUser(AbstractUser):
    wallet_address = models.CharField(max_length=42, unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Adding related_name to avoid clash
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Adding related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class Hub(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paragraph_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Add this field
    text_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.paragraph_name

class Event(models.Model):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='joined_events', blank=True)

    def __str__(self):
        return self.event_name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
