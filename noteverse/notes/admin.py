from django.contrib import admin
from .models import Category, SubCategory, SharedStatus, Tag, Note, Comment

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'thumbnail']
    search_fields = ['title']
    list_filter = ['title']

# SubCategory Admin
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'description', 'thumbnail']
    search_fields = ['title', 'category__title']
    list_filter = ['category', 'title']


# SharedStatus Admin
@admin.register(SharedStatus)
class SharedStatusAdmin(admin.ModelAdmin):
    list_display = ['shared_by', 'shared_with', 'note', 'permissions', 'shared_at']
    search_fields = ['shared_by__username', 'shared_with__username', 'note__title']
    list_filter = ['permissions', 'shared_at']

# Tag Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at', 'updated_at']

# Note Admin
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'visibility', 'category', 'subcategory', 'views']
    search_fields = ['title', 'owner__username', 'category__title', 'subcategory__title']
    list_filter = ['owner', 'category', 'subcategory', 'visibility', 'views']

# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['note', 'user', 'text', 'created_at', 'updated_at', 'parent_comment']
    search_fields = ['note__title', 'user__username', 'text']
    list_filter = ['created_at', 'updated_at']

