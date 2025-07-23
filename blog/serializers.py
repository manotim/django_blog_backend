from rest_framework import serializers
from .models import Category, News, Comment, Like
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'category', 'category_id',
            'author', 'image', 'body', 'date_posted',
            'updated_at', 'is_breaking', 'likes_count', 'comments_count'
        ]

    def get_likes_count(self, obj):
        return obj.like_set.filter(is_liked=True).count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'news', 'user', 'name', 'email', 'comment', 'timestamp', 'user_name']
        read_only_fields = ['user', 'timestamp', 'user_name']

    def get_user_name(self, obj):
        if obj.user:
            return obj.user.username
        return obj.name  # fallback if anonymous


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'news', 'is_liked', 'timestamp']
