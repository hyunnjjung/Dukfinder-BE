from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1대1 모델 확장
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # primary_key를 User의 pk로 설정하여 통합적으로 관리
    image = models.ImageField(upload_to='profile/', default='default.png')

#User 모델이 post_save 이벤트를 발생시켰을 때 해당 이벤트가 일어났다는 사실을 받아서, 해당 유저 인스턴스와 연결되는 Profile 데이터를 생성
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)