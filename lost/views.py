
from rest_framework import generics, permissions, viewsets
from rest_framework.generics import CreateAPIView

from .models import LostPost, Comment, Reply
from django.utils import timezone
from datetime import timedelta
from .serializers import LostPostSerializer, CommentSerializer, ReplySerializer
from django.db.models import Q


class CustomReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_superuser


class CategoryPostsView(generics.ListAPIView):
    serializer_class = LostPostSerializer
    permission_classes = [CustomReadOnly]

    def get_queryset(self):
        category = self.kwargs['category']
        return LostPost.objects.filter(category=category)


class LostPostListView(generics.ListAPIView): #lostpostlist
    queryset = LostPost.objects.order_by('-created_at')
    serializer_class = LostPostSerializer
    permission_classes = [CustomReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LostPostDetailView(generics.RetrieveDestroyAPIView): #Findpostlistdetail, destory
    queryset = LostPost.objects.all()
    serializer_class = LostPostSerializer
    permission_classes = [CustomReadOnly]


class LostPostCreateView(CreateAPIView): #lostpostlistcreate
    queryset = LostPost.objects.all()
    serializer_class = LostPostSerializer
    permission_classes = [CustomReadOnly]

class LostPostUpdateView(generics.RetrieveUpdateAPIView):
    queryset = LostPost.objects.all()
    serializer_class = LostPostSerializer
    lookup_url_kwarg = 'intLpk'
    permission_classes = [CustomReadOnly]

class ThisWeekPostsListView(generics.ListAPIView):
    serializer_class = LostPostSerializer
    permission_classes = [CustomReadOnly]
    def get_queryset(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        queryset = LostPost.objects.filter(created_at__range=[start_of_week, end_of_week])
        return queryset

class ThisMonthPostsListView(generics.ListAPIView):
    serializer_class = LostPostSerializer
    permission_classes = [CustomReadOnly]
    def get_queryset(self):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(days=1)

        queryset = LostPost.objects.filter(created_at__range=[start_of_month, end_of_month])
        return queryset

class LostPostSearchAPIView(generics.ListAPIView):
    serializer_class = LostPostSerializer
    permission_classes = [CustomReadOnly]
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return LostPost.objects.filter(Q(title__icontains=query))


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.prefetch_related('replys')
    serializer_class = CommentSerializer
    permission_classes = [CustomReadOnly]


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [CustomReadOnly]