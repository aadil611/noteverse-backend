import pytest
from django.contrib.auth import get_user_model
from notes.models import Category, SubCategory, Tag, Note, Comment, SharedStatus

User = get_user_model()

@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(title="Category 1", description="Description")
    assert category.title == "Category 1"

@pytest.mark.django_db
def test_subcategory_creation():
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    assert subcategory.title == "SubCategory 1"


@pytest.mark.django_db
def test_tag_creation():
    tag = Tag.objects.create(name="Tag 1")
    assert tag.name == "Tag 1"

@pytest.mark.django_db
def test_note_creation():
    user = User.objects.create_user(email="user@domain.com", password="password")
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user, category=category, subcategory=subcategory,
    )
    assert note.title == "Note 1"

@pytest.mark.django_db
def test_comment_creation():
    user = User.objects.create_user(email="user@domain.com", password="password")
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user, category=category, subcategory=subcategory
    )
    comment = Comment.objects.create(note=note, user=user, text="This is a comment")
    assert comment.text == "This is a comment"

@pytest.mark.django_db
def test_shared_status_creation():
    user1 = User.objects.create_user(email="user1@domain.com", password="password")
    user2 = User.objects.create_user(email="user2@domain.com", password="password")
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user1, category=category, subcategory=subcategory
    )
    shared_status = SharedStatus.objects.create(shared_by=user1, shared_with=user2, permissions='view', note=note)
    assert shared_status.shared_by == user1
