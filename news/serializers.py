from .models import Post, Comment
from .models import *
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'heading', 'content', 'rate', 'author_id', 'property', 'category']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'rate']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name']