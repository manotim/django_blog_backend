from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from .models import Category, News, Comment, Like
from .serializers import (
    CategorySerializer, NewsSerializer,
    CommentSerializer, LikeSerializer
)
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404



# ✅ Registration Serializer
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

# ✅ Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read for anonymous, write for auth

    def get_queryset(self):
        queryset = News.objects.all()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        news = self.get_object()
        user = request.user

        like_obj, created = Like.objects.get_or_create(news=news, user=user)
        if not created:
            like_obj.delete()
            liked = False
        else:
            liked = True

        return Response({
            "liked": liked,
            "likes_count": news.like_set.count()
        })


# ✅ Move this outside the class
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def comments(request, slug):
    news = get_object_or_404(News, slug=slug)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.save(
                    news=news,
                    user=request.user,
                    name=request.user.username,
                    email=request.user.email
                )
            else:
                serializer.save(news=news)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET request - list comments
    comments = news.comments.all().order_by('-timestamp')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
