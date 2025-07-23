import uuid
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    News categories like: Business, Politics, Sports, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class News(models.Model):
    """
    The core news model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='news')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    image = models.ImageField(upload_to='news_images/')
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_breaking = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_posted']
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Comments left by users on news.
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.news.title}'


class Like(models.Model):
    """
    Track likes and unlikes on a news post.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'news')

    def __str__(self):
        return f"{self.user.username} - {self.news.title} - {'Like' if self.is_liked else 'Unlike'}"
