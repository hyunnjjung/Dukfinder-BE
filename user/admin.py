from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

# admin에서 기본 User와 Profile이랑 같이 보이도록 하기 위해
class ProfileInline(admin.StackedInline):
    model = Profile 
    can_delete = False # 관리자 패널에서 profile 객체 삭제 못하게 
    verbose_name_plural = "profile"  # 복수형으로 이름 표기하지 않도록 직접 지정


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)