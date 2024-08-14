from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, TagViewSet, CategoryViewSet, SubCategoryViewSet, SharedStatusViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'tags', TagViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'sharedstatuses', SharedStatusViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
