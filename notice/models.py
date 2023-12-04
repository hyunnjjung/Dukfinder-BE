from django.db import models
from django.contrib.auth.models import User
import os

class NoticePost(models.Model): # 공지사항 포스트 모델
    title = models.CharField(max_length=30, blank=True) # 제목

    content = models.TextField() # 내용

    
    notice_image = models.ImageField(upload_to='notice/images/%Y/%m/%d/', blank=True)
    top_fixed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # 작성자

    view_count = models.IntegerField(default=0) #조회수

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/notice/{self.pk}/'
