from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, UserinfoSerializer, PasswordSerializer
from .models import Profile
from .permissions import CustomReadOnly
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated, AllowAny

# 로그인
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

# 내가 쓴 글 리스트
from lost.models import LostPost
from lost.serializers import LostPostSerializer
from find.models import FindPost
from find.serializers import FindPostSerializer

from rest_framework.views import APIView

# 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# 로그인
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data  # validate()의 리턴값인 token을 받아온다.
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
# 프로필    
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CustomReadOnly] # 본인만 프로필 수정 가능하도록 권한 설정

# 유저 이름과 이메일 가져오기/회원탈퇴/로그아웃
class UserinfoView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserinfoSerializer

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        serialized_data = {'username': serializer.data.get('username', ''),
                           'email': serializer.data.get('email', '')}
        return Response(serialized_data)

    def delete(self, request):
        user = request.user
        if user:
            user.delete()
            return Response({"message": "회원탈퇴 성공"}, status=status.HTTP_200_OK)
        return Response({"message": "회원탈퇴 실패"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = request.user
        if user:
            logout(request)
            data = {'success': '로그아웃 성공'}
            return Response(data=data, status=status.HTTP_200_OK)
        data = {'success': '로그아웃 실패'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

# 비밀번호 변경
class PasswordView(generics.UpdateAPIView):
    serializer_class = PasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # 원래 비번과 맞는지 확인
            if not user.check_password(old_password):
                return Response({'detail': '원래 비밀번호와 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({'detail': '비밀번호 변경 성공'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 마이페이지에서 쓸 리스트 및 일괄 처리들
class MyLostListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LostPostSerializer

    def get_queryset(self):
        user = self.request.user
        return LostPost.objects.filter(author=user)

    def get(self, request):
        user = request.user
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MyFindListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FindPostSerializer

    def get_queryset(self):
        user = self.request.user
        return FindPost.objects.filter(author=user)

    def get(self, request):
        user = request.user
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class BulkDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        lost_ids = kwargs.get('lost_ids', '').split(',')
        find_ids = kwargs.get('find_ids', '').split(',')

        lost_queryset = LostPost.objects.filter(author=user, id__in=lost_ids)
        find_queryset = FindPost.objects.filter(author=user, id__in=find_ids)

        if not lost_queryset.exists() or not find_queryset.exists():
            return Response({"detail": "Invalid post selection."}, status=status.HTTP_400_BAD_REQUEST)

        # 일괄적으로 lost posts 삭제
        lost_queryset.delete()

        # 일괄적으로 find posts 삭제
        find_queryset.delete()

        return Response({"detail": "삭제 성공"}, status=status.HTTP_204_NO_CONTENT)

# found_status 일괄 변경 처리
class UpdateFoundStatusBulkView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk_ids):
        ids = [int(pk) for pk in pk_ids.split(',')]
        user = request.user

        queryset = LostPost.objects.filter(id__in=ids, author=user)

        if not queryset.exists():
            return Response({"detail": "해당 글이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 일괄적으로 found_status를 "찾음"으로 변경
        queryset.update(found_status="찾음")

        return Response({"detail": "찾음으로 변경 완료"}, status=status.HTTP_200_OK)