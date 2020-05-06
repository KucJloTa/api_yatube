from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from django.urls import path, include
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]