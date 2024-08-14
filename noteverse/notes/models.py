from django.db import models
from django.contrib.auth import get_user_model
from .choices import VISIBILITY_CHOICES

User = get_user_model()

# Category Model
class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='category_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title

# SubCategory Model
class SubCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='subcategory_thumbnails/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        unique_together = ('title', 'category')

    def __str__(self):
        return f"{self.title} - {self.category.title}"


# SharedStatus Model
class SharedStatus(models.Model):
    PERMISSIONS = [
        ('view', 'View'),
        ('edit', 'Edit'),
    ]
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_shared_notes')
    permissions = models.CharField(max_length=4, choices=PERMISSIONS)
    note = models.ForeignKey('Note', on_delete=models.CASCADE, related_name='shared_statuses')
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note.title} shared by {self.shared_by.username} with {self.shared_with.username}"

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Note Model
class Note(models.Model):

    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, related_name='notes', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='note_thumbnails/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    likes = models.ManyToManyField(User, related_name='liked_notes', blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_notes', blank=True)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='notes')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='notes')
    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES, default=VISIBILITY_CHOICES[0][0])

    def __str__(self):
        return self.title

# Comment Model
class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.note.title}"

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
