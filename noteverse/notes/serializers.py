from rest_framework import serializers
from .models import Category, SubCategory, SharedStatus, Tag, Note, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'thumbnail']
        
    

# SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'description', 'thumbnail', 'category']



# SharedStatus Serializer
# class SharedStatusSerializer(serializers.ModelSerializer):
#     shared_by = serializers.StringRelatedField()
#     shared_with = serializers.StringRelatedField()
#     note = serializers.StringRelatedField()

#     class Meta:
#         model = SharedStatus
#         fields = ['id', 'shared_by', 'shared_with', 'permissions', 'shared_at', 'note']


class SharedStatusSerializer(serializers.ModelSerializer):
    # shared_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # shared_with = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # note = serializers.PrimaryKeyRelatedField(queryset=Note.objects.all())
    shared_by = serializers.StringRelatedField()
    shared_with = serializers.StringRelatedField()
    note = serializers.StringRelatedField()

    class Meta:
        model = SharedStatus
        fields = ['id', 'shared_by', 'shared_with', 'permissions', 'shared_at', 'note']


# Tag Serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at', 'updated_at']

# Note Serializer
class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    favorites_count = serializers.IntegerField(source='favorites.count', read_only=True)
    shared_statuses = SharedStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = [
            'id', 'title', 'tags', 'thumbnail', 'description', 'data', 
            'owner', 'shared_statuses', 'likes_count', 'favorites_count', 
            'views', 'visibility', 'category', 'subcategory','created_at','updated_at'
        ]

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'note', 'user', 'text', 'created_at', 'updated_at', 'parent_comment', 'replies']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return None
