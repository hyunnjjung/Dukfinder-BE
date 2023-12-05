from rest_framework import serializers
from .models import FindPost, FindComment, FindReply


class FindReplySerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField()
    class Meta:
        model = FindReply
        fields = ('id', 'user_id', 'comment_id', 'content', 'created_at', 'updated_at')


class FindCommentSerializer(serializers.ModelSerializer):
    replys = FindReplySerializer(many=True, read_only=True)
    user_id = serializers.StringRelatedField()

    class Meta:
        model = FindComment
        fields = ('id', 'user_id', 'post_id', 'content', 'created_at', 'updated_at', 'replys')



class FindPostSerializer(serializers.ModelSerializer):
    comments = FindCommentSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()
    class Meta:
        model = FindPost
        fields = ('id', 'comments', 'title', 'content', 'head_image', 'created_at', 'updated_at', 'author', 'date_select', 'category', 'location', 'LostAndFound')