from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagersTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="user@domain.com", password="password")
        self.assertEqual(user.email, "user@domain.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        # Ensure that the username field is not present
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        
        # ensure that the user is not created without an email and password
        with self.assertRaises(TypeError):
            User.objects.create_user()
        
        # Ensure that the user is not created with a blank password
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
            
        # Ensure that the user is not created with a blank email
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="password")
            
    
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@domain.com", password="password")
        self.assertEqual(admin_user.email, "super@domain.com", "password")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="super@domain.com", password="password", is_superuser=False)