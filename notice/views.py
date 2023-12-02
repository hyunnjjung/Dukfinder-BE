from django.shortcuts import redirect
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import NoticePost
from .serializers import NoticePostSerializer, NoticePostListSerializer

class IsStaffOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)

class NoticePostListView(generics.ListAPIView): #공지사항 리스트
    queryset = NoticePost.objects.order_by('-top_fixed', '-created_at')
    serializer_class = NoticePostListSerializer
    permission_classes = [permissions.IsAuthenticated]

class NoticePostCreateView(generics.CreateAPIView):
    queryset = NoticePost.objects.all()
    serializer_class = NoticePostSerializer
    permission_classes = [IsStaffOrSuperuser]

    def perform_create(self, serializer):
        serializer.save()
        return HttpResponseRedirect(reverse('notice-list'))

class NoticePostDetailView(generics.RetrieveDestroyAPIView):
    queryset = NoticePost.objects.all()
    serializer_class = NoticePostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        serializer.increase_views(instance)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        if self.request.user.is_staff or self.request.user.is_superuser:
            instance.delete()
            return HttpResponseRedirect(reverse('notice-list'))
        else:
            return Response({"detail": "You do not have permission to delete this notice."}, status=403)
