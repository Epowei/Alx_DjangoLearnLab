from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import feed

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

app_name = 'posts'

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', feed, name='feed'),
]