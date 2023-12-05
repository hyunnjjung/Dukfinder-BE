
from rest_framework import generics, permissions, viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import LostPost, Comment, Reply
from django.utils import timezone
from datetime import timedelta
from .serializers import LostPostSerializer, CommentSerializer, ReplySerializer
from django.db.models import Q



class CategoryPostsView(generics.ListAPIView):
    serializer_class = LostPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        category = self.kwargs['category']
        return LostPost.objects.filter(category=category).order_by('created_at')


class LostPostListView(generics.ListAPIView): #lostpostlist
    queryset = LostPost.objects.order_by('-created_at')
    serializer_class = LostPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LostPostDetailView(generics.RetrieveDestroyAPIView): #Findpostlistdetail, destory
    queryset = LostPost.objects.all()
    serializer_class = LostPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        user = self.request.user
        if user == instance.author or user.is_staff or user.is_superuser:
            instance.delete()
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to delete this post.")


class LostPostCreateView(CreateAPIView): #lostpostlistcreate
    queryset = LostPost.objects.all()
    serializer_class = LostPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # 현재 로그인한 사용자의 ID를 Comment 객체에 저장
        serializer.save(author=self.request.user)

class LostPostUpdateView(generics.RetrieveUpdateAPIView):
    queryset = LostPost.objects.all()
    serializer_class = LostPostSerializer
    lookup_url_kwarg = 'intLpk'

    def perform_update(self, serializer):
        user = self.request.user

        if user == serializer.instance.author or user.is_staff or user.is_superuser:
            serializer.save()
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to update this post.")

class ThisWeekPostsListView(generics.ListAPIView):
    serializer_class = LostPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)

        queryset = LostPost.objects.filter(created_at__range=[start_of_week, end_of_week]).order_by('created_at')
        return queryset

class ThisMonthPostsListView(generics.ListAPIView):
    serializer_class = LostPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(days=1)

        queryset = LostPost.objects.filter(created_at__range=[start_of_month, end_of_month]).order_by('created_at')
        return queryset

class LostPostSearchAPIView(generics.ListAPIView):
    serializer_class = LostPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return LostPost.objects.filter(Q(title__icontains=query)).order_by('created_at')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.prefetch_related('replys')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_pk)

    def perform_create(self, serializer):
        new_comment = serializer.save(user_id=self.request.user)
        comment_id = new_comment.id

        # Modify the response data to include the comment_id
        response_data = {
            'id': comment_id,
            'message': 'Comment created successfully',  # You can customize the message
            # Add any other fields you want to include in the response
        }

        return Response(response_data, status=status.HTTP_201_CREATED)



class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return Reply.objects.filter(comment=post_pk)


    def perform_create(self, serializer):

        serializer.save(user_id=self.request.user)