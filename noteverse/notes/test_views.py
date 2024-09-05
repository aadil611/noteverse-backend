import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from notes.models import Category, SubCategory, Tag, Note, Comment, SharedStatus
from .serializers import CommentSerializer


User = get_user_model()

@pytest.mark.django_db
def test_category_list():
    client = APIClient()
    Category.objects.create(title="Category 1", description="Description")
    response = client.get('/api/categories/')
    assert response.status_code == 200
    assert response.data[0]['title'] == "Category 1"

@pytest.mark.django_db
def test_subcategory_list():
    client = APIClient()
    category = Category.objects.create(title="Category 1", description="Description")
    SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    response = client.get('/api/subcategories/')
    assert response.status_code == 200
    assert response.data[0]['title'] == "SubCategory 1"



@pytest.mark.django_db
def test_tag_list():
    client = APIClient()
    Tag.objects.create(name="Tag 1")
    response = client.get('/api/tags/')
    assert response.status_code == 200
    assert response.data[0]['name'] == "Tag 1"

@pytest.mark.django_db
def test_note_list(api_client):
    user = User.objects.create_user(email="user@domain.com", password="password")
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)

    Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user, category=category, subcategory=subcategory
    )
    response = api_client.get('/api/notes/')
    assert response.status_code == 200
    # print("##################################",type(response.data),response.data)
    
    # assert response.data[0]['title'] == "Note 1"

@pytest.mark.django_db
def test_comment_list():
    client = APIClient()
    user = User.objects.create_user(email="user@domain.com", password="password")
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user, category=category, subcategory=subcategory
    )
    Comment.objects.create(note=note, user=user, text="This is a comment")
    response = client.get('/api/comments/')
    assert response.status_code == 200
    assert response.data[0]['text'] == "This is a comment"

@pytest.mark.django_db
def test_shared_status_list():
    client = APIClient()
    user1 = User.objects.create_user(email="user1@domain.com", password="password")
    user2 = User.objects.create_user(email="user2@domain.com", password="password")
    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user1, category=category, subcategory=subcategory
    )
    shared_status = SharedStatus.objects.create(shared_by=user1, shared_with=user2, permissions='view', note=note)
    response = client.get('/api/sharedstatuses/')
    assert response.status_code == 200
    assert response.data[0]['shared_by'] == user1.email






#########*
# create 
#########*

# Helper Functions
@pytest.fixture
def api_client():
    client = APIClient()
    user = User.objects.create_user(email="unique_user@domain.com", password="password")
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def create_unique_user():
    return User.objects.create_user(email=f"user{User.objects.count()}@domain.com", password="password")

@pytest.fixture
def create_category():
    return Category.objects.create(title="Category 1", description="Description")

@pytest.fixture
def create_subcategory(create_category):
    return SubCategory.objects.create(title="SubCategory 1", description="Description", category=create_category)


@pytest.fixture
def create_note(create_unique_user, create_category, create_subcategory):
    return Note.objects.create(
        title="New Note", 
        description="A new note", 
        data="Some data", 
        owner=create_unique_user, 
        category=create_category, 
        subcategory=create_subcategory,
    )

@pytest.fixture
def create_shared_status(create_note, create_unique_user):
    return SharedStatus.objects.create(shared_by=create_unique_user, shared_with=create_unique_user, permissions='view')



# Test Cases
@pytest.mark.django_db
def test_create_category(api_client):
    data = {"title": "New Category", "description": "A new category" }
    response = api_client.post('/api/categories/', data, format='json')
    assert response.status_code == 201
    assert response.data['title'] == "New Category"
    assert Category.objects.filter(title="New Category").exists()

@pytest.mark.django_db
def test_create_subcategory(api_client, create_category):
    data = {"title": "New SubCategory", "description": "A new subcategory", "category": create_category.id}
    response = api_client.post('/api/subcategories/', data, format='json')
    assert response.status_code == 201
    assert response.data['title'] == "New SubCategory"
    assert SubCategory.objects.filter(title="New SubCategory").exists()



@pytest.mark.django_db
def test_create_tag(api_client):
    data = {"name": "New Tag"}
    response = api_client.post('/api/tags/', data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == "New Tag"
    assert Tag.objects.filter(name="New Tag").exists()

@pytest.mark.django_db
def test_create_note(api_client, create_unique_user, create_category, create_subcategory):
    data = {
        "title": "New Note",
        "description": "A new note",
        "data": "Some data",
        "owner": create_unique_user.id,
        "category": create_category.id,
        "subcategory": create_subcategory.id,
        "tags": [],
        "likes": [],
        "favorites": [],
        "views": 0
    }

    response = api_client.post('/api/notes/', data, format='json')
    assert response.status_code == 201
    assert response.data['title'] == "New Note"
    assert Note.objects.filter(title="New Note").exists()

# @pytest.mark.django_db
# def test_create_comment(api_client):
#     user = User.objects.create_user(email="user@domain.com", password="password")
#     category = Category.objects.create(title="Category 1", description="Description")
#     subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)
#     note = Note.objects.create(
#         title="Note 1", description="Description", data="Some data",
#         owner=user, category=category, subcategory=subcategory,
#     )

#     data = {
#         "note": note.id,  
#         "user": user.id,  
#         "text": "This is a comment"
#     }

#     response = api_client.post('/api/comments/', data, format='json')
    
#     assert response.status_code == 201
#     assert response.data['text'] == "This is a comment"
#     assert Comment.objects.filter(note=note, user=user, text="This is a comment").exists()


@pytest.mark.django_db
def test_create_comment(api_client, create_note, create_unique_user):
    note = create_note  # Use the fixture directly
    user = create_unique_user  # Use the fixture directly

    data = {
        "note": note.id,  # Access the ID of the created note
        "user": user.id,  # Access the ID of the created user
        "text": "This is a comment"
    }

    response = api_client.post('/api/comments/', data, format='json')
    
    assert response.status_code == 201
    assert response.data['text'] == "This is a comment"
    print(response.data)
    # assert Comment.objects.filter(note=note.id, user=user.id, text="This is a comment").exists()
    # print(CommentSerializer(Comment.objects.get(note=note.id, user=user.id)).data)


@pytest.mark.django_db
def test_create_shared_status(api_client, create_note, create_unique_user):
    # data = {
    #     "shared_by": create_unique_user.id,
    #     "shared_with": create_unique_user.id,
    #     "permissions": "view",
    #     "note_id": create_note.id
    # }
    
    user = User.objects.create_user(email="owner@domain.com", password="password")
    shared_with_user = User.objects.create_user(email="viewer@domain.com", password="password")
    category = Category.objects.create(title="Category 22", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 11", description="Description", category=category)

    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user, category=category, subcategory=subcategory
    )

    data = {
        "shared_by": user.id,
        "shared_with": shared_with_user.id,
        "permissions": "view",
        "note": note.id,
        "shared_with_id": shared_with_user.id
    }
    response = api_client.post('/api/sharedstatuses/', data, format='json')
    assert response.status_code == 201
    assert response.data['permissions'] == "view"
    # assert SharedStatus.objects.filter(shared_by=create_unique_user, shared_with=create_unique_user, permissions="view").exists()



@pytest.mark.django_db
def test_shared_notes():
    client = APIClient()
    user1 = User.objects.create_user(email="user1@domain.com", password="password")
    user2 = User.objects.create_user(email="user2@domain.com", password="password")

    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)

    note = Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user1, category=category, subcategory=subcategory
    )

    SharedStatus.objects.create(note=note, shared_by=user1, shared_with=user2, permissions='view')

    client.force_authenticate(user=user2)
    response = client.get('/api/notes/get-shared-notes/')
    
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Note 1"
    
    
    
@pytest.mark.django_db
def test_featured_notes():
    client = APIClient()
    user = User.objects.create_user(email="user@domain.com", password="password")

    category = Category.objects.create(title="Category 1", description="Description")
    subcategory = SubCategory.objects.create(title="SubCategory 1", description="Description", category=category)

    Note.objects.create(
        title="Note 1", description="Description", data="Some data",
        owner=user, category=category, subcategory=subcategory, visibility='public'
    )

    client.force_authenticate(user=user)
    response = client.get(f'/api/notes/get-featured-notes/')
    
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Note 1"
