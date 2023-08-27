from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Post
from .serializers import PostsSerializer, PostDetailSerializer

# Create your views here.

class Posts(APIView):
    def get(self, request):
        all_posts = Post.objects.all()
        serializer = PostsSerializer(all_posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostDetailSerializer(data = request.data)
        if serializer.is_valid():
            title = request.data.get("title")
            content = request.data.get("content")
            post = serializer.save(title=title, content=content)
            return Response(PostDetailSerializer(post).data)
        else:
            return Response(serializer.errors)
        
class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        post = self.get_object(pk)
        return Response(PostDetailSerializer(post).data)
    
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            updated_post = serializer.save()
            return Response(PostDetailSerializer(updated_post).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        
        all_posts = Post.objects.all()
        serializer = PostsSerializer(all_posts, many=True)
        return Response(serializer.data)