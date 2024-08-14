from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from .models import Category, SubCategory, SharedStatus, Tag, Note, Comment
from .serializers import (
    CategorySerializer, SubCategorySerializer,
    SharedStatusSerializer, TagSerializer, NoteSerializer, CommentSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# SubCategory ViewSet
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# SharedStatus ViewSet
class SharedStatusViewSet(viewsets.ModelViewSet):
    queryset = SharedStatus.objects.all()
    serializer_class = SharedStatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(shared_by=self.request.user)

# Tag ViewSet
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Note ViewSet
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Note.objects.all()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(visibility='public')

# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        note_id = self.request.query_params.get('note_id')
        if note_id:
            return Comment.objects.filter(note_id=note_id)
        return super().get_queryset()
