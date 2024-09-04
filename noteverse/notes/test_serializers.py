import pytest
from django.contrib.auth import get_user_model
from notes.models import Category, SubCategory, Tag, Note, Comment, SharedStatus
from notes.serializers import CategorySerializer, SubCategorySerializer, TagSerializer, NoteSerializer, CommentSerializer, SharedStatusSerializer

User = get_user_model()

@pytest.mark.django_db
def test_category_serializer():
    category = Category.objects.create(title="Category 1", description="Description")
    serializer = CategorySerializer(category)
    assert serializer.data["title"] == "Category 1"
    assert serializer.data["description"] == "Description"

@pytest.mark.django_db
def test_subcategory_serializer():
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    serializer = SubCategorySerializer(subcategory)
    assert serializer.data["title"] == "SubCategory 1"
    assert serializer.data["description"] == "Description"


@pytest.mark.django_db
def test_tag_serializer():
    tag = Tag.objects.create(name="Tag 1")
    serializer = TagSerializer(tag)
    assert serializer.data["name"] == "Tag 1"

@pytest.mark.django_db
def test_note_serializer():
    user = User.objects.create_user(email="user@domain.com", password="password")
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user, category=category, subcategory=subcategory
    )
    serializer = NoteSerializer(note)
    assert serializer.data["title"] == "Note 1"
    assert serializer.data["description"] == "Description"

@pytest.mark.django_db
def test_comment_serializer():
    user = User.objects.create_user(email="user@domain.com", password="password")
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user, category=category, subcategory=subcategory
    )
    comment = Comment.objects.create(note=note, user=user, text="This is a comment")
    serializer = CommentSerializer(comment)
    assert serializer.data["text"] == "This is a comment"

@pytest.mark.django_db
def test_shared_status_serializer():
    user1 = User.objects.create_user(email="user1@domain.com", password="password")
    user2 = User.objects.create_user(email="user2@domain.com", password="password")
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)

    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user1, category=category, subcategory=subcategory
    )
    shared_status = SharedStatus.objects.create(shared_by=user1, shared_with=user2, permissions='view', note=note)
    serializer = SharedStatusSerializer(shared_status)
    assert serializer.data["shared_by"] == user1.email
    assert serializer.data["shared_with"] == user2.email
