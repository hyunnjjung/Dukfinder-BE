from django.contrib.auth.models import User  # 장고의 기본 User 모델 사용
from django.contrib.auth.password_validation import validate_password  # Django의 기본 pw 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token  # Token 모델
from rest_framework.validators import UniqueValidator  # 이메일 중복 방지를 위한 검증 도구
from django.contrib.auth import authenticate
# Django의 기본 authenticate 함수 -> 우리가 설정한 DefaultAuthBackend인 TokenAuth 방식으로 유저를 인증해준다.

from .models import Profile

# 회원가입
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, # 필수 항목 의미
        validators=[UniqueValidator(queryset=User.objects.all())],  # 이메일에 대한 중복 검증
    )
    password = serializers.CharField(
        write_only=True, # 비밀번호는 쓰기만 되도록
        required=True,
        validators=[validate_password],  # 비밀번호에 대한 검증
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data): 
        # password과 password2의 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."})
        
        # 덕성 이메일인지
        if not data.get("email", "").endswith("@duksung.ac.kr"):
            raise serializers.ValidationError(
                detail={"error": "덕성 이메일만 가입할 수 있습니다."}
            )

        return data

    def create(self, validated_data):
        # CREATE 요청에 대해 create 메서드를 오버라이딩해 유저를 생성하고 토큰도 생성하게 해준다.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        
        return user

# 로그인
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    # write_only=True 옵션을 통해 클라이언트->서버의 역직렬화는 가능하지만, 서버->클라이언트 방향의 직렬화는 불가능(보안 위해)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)  # 해당 유저의 토큰을 불러옴
            return token
        raise serializers.ValidationError(  # 가입된 유저가 없을 경우
            {"error": "가입된 회원이 아닙니다."}
        )

# 프로필 사진
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("image", )

# 유저 이름, 이메일
class UserinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

# 비밀번호
class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("old_password", "new_password")