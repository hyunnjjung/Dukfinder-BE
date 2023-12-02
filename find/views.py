
from rest_framework import generics, permissions, viewsets
from rest_framework.generics import CreateAPIView

from .models import FindPost, FindComment, FindReply
from django.utils import timezone
from datetime import timedelta
from .serializers import FindPostSerializer, FindCommentSerializer, FindReplySerializer
from django.db.models import Q


class CustomReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'DELETE':
            return obj.user == request.user or request.user.is_superuser
        else:
            return obj.user == request.user or request.user.is_superuser


class CategoryPostsView(generics.ListAPIView):
    serializer_class = FindPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        category = self.kwargs['category']
        return FindPost.objects.filter(category=category)


class FindPostListView(generics.ListAPIView): #lostpostlist
    queryset = FindPost.objects.order_by('-created_at')
    serializer_class = FindPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FindPostDetailView(generics.RetrieveDestroyAPIView): #Findpostlistdetail, destory
    queryset = FindPost.objects.all()
    serializer_class = FindPostSerializer
    permission_classes = [CustomReadOnly]

class FindPostCreateView(CreateAPIView): #lostpostlistcreate
    queryset = FindPost.objects.all()
    serializer_class = FindPostSerializer
    permission_classes = [permissions.IsAuthenticated]

class FindPostUpdateView(generics.RetrieveUpdateAPIView):
    queryset = FindPost.objects.all()
    serializer_class = FindPostSerializer
    permission_classes = [CustomReadOnly]
    lookup_url_kwarg = 'intLpk'

class ThisWeekPostsListView(generics.ListAPIView):
    serializer_class = FindPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        queryset = FindPost.objects.filter(created_at__range=[start_of_week, end_of_week])
        return queryset

class ThisMonthPostsListView(generics.ListAPIView):
    serializer_class = FindPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(days=1)

        queryset = FindPost.objects.filter(created_at__range=[start_of_month, end_of_month])
        return queryset

class FindPostSearchAPIView(generics.ListAPIView):
    serializer_class = FindPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return FindPost.objects.filter(Q(title__icontains=query))


class FindCommentViewSet(viewsets.ModelViewSet):
    queryset = FindComment.objects.prefetch_related('replys')
    serializer_class = FindCommentSerializer
    permission_classes = [CustomReadOnly]


class FindReplyViewSet(viewsets.ModelViewSet):
    queryset = FindReply.objects.all()
    serializer_class = FindReplySerializer
    permission_classes = [CustomReadOnly]