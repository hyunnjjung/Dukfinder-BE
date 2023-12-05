from rest_framework import serializers
from .models import LostPost, Comment, Reply


class ReplySerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField()
    class Meta:
        model = Reply
        fields = ('user_id', 'comment_id', 'content', 'created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    replys = ReplySerializer(many=True, read_only=True)
    user_id = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('user_id', 'post_id', 'content', 'created_at', 'updated_at', 'replys')



class LostPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()
    class Meta:
        model = LostPost
        fields = ("title", "content", "head_image", "created_at", "updated_at", "author", "date_select", "category", "location", "found_status" , "comments")
