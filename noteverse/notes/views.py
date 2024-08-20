from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
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
    
        
    
    @action(detail=False, methods=['get'], url_path='get-shared-notes')
    def shared_notes(self, request):
        if not self.request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)
        shared_statuses = SharedStatus.objects.filter(shared_with=self.request.user)
        shared_notes = [status.note for status in shared_statuses]
        serializer = NoteSerializer(shared_notes, many=True)
        return Response(serializer.data)
    
    
    @action(detail=False, methods=['get'], url_path='get-featured-notes')
    def featured_notes(self, request):
        featured_notes = Note.objects.filter(visibility='public')
        serializer = NoteSerializer(featured_notes, many=True)
        return Response(serializer.data)

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
