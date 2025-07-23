# blog/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    CategoryViewSet,
    NewsViewSet,
    CommentViewSet,
    LikeViewSet,
    RegisterView,
    comments,  # ✅ Import the custom comment view
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'news', NewsViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    # ✅ ViewSets
    path('', include(router.urls)),

    # ✅ JWT Auth Endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Custom comments endpoint per news item (GET/POST)
    path('news/<slug:slug>/comments/', comments, name='news-comments'),
]
