from rest_framework import serializers
from .models import NoticePost

class NoticePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoticePost
        fields = ('id', 'title', 'content', 'notice_image', 'top_fixed', 'created_at', 'author')

    def increase_views(self, instance):
        instance.view_count += 1
        instance.save(update_fields=['view_count'])


class NoticePostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticePost
        fields = '__all__'