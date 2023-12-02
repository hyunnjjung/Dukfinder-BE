from django.db import models
from django.contrib.auth.models import User


class FindPost(models.Model):
    title = models.CharField(max_length=30, blank=True)

    content = models.TextField()

    head_image = models.ImageField(upload_to='find/images/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    date_select = models.DateField(blank=True, null=True)

    CATEGORY_CHOICES = [
        ('전자기기', '전자기기'),
        ('지갑/카드', '지갑/카드'),
        ('악세사리', '악세사리'),
        ('화장품', '화장품'),
        ('기타', '기타'),
    ]

    category = models.CharField(max_length=20, blank=True, null=True, choices=CATEGORY_CHOICES)

    LOCATION_CHOICES = [
        ('정문·대학본부', '정문·대학본부'),
        ('후문', '후문'),
        ('인문사회관', '인문사회관'),
        ('대강의동', '대강의동'),
        ('차마리사기념관', '차미리사기념관'),
        ('학생회관', '학생회관'),
        ('도서관·대학원', '도서관·대학원'),
        ('예술관', '예술관'),
        ('자연관', '자연관'),
        ('약학관', '약학관'),
        ('기타', '기타'),
    ]

    location = models.CharField(max_length=20, blank=True, null=True, choices=LOCATION_CHOICES)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

class FindComment(models.Model):
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post_id = models.ForeignKey(FindPost, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 대댓글(답글)
class FindReply(models.Model):
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(FindComment, related_name='replys', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)