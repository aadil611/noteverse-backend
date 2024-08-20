import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_list_viewset_authenticated():
    client = APIClient()
    
    # Create users
    user1 = User.objects.create_user(email="user1@domain.com", password="password", is_active=True)
    user2 = User.objects.create_user(email="user2@domain.com", password="password", is_active=False)
    
    # Authenticate as user1
    client.force_authenticate(user=user1)
    
    # Test list view
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert len(response.data) == 1  # only active  users should be listed
    
    # Test retrieve view
    response = client.get(f'/api/users/{user2.email}/')
    assert response.status_code == 200
    assert response.data['email'] == user2.email

