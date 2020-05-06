from django.shortcuts import render
from posts.models import Post, Comment
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permission import IsAuthorOrReadOnly
from rest_framework.exceptions import PermissionDenied


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied
        return serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied
        return instance.delete()



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return Comment.objects.filter(post=post)
    
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied
        return serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied
        return instance.delete()
