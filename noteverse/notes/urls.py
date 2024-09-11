from rest_framework.routers import DefaultRouter,path
from .views import NoteViewSet, TagViewSet, CategoryViewSet, SubCategoryViewSet, SharedStatusViewSet, CommentViewSet, comment_reply, like_note_view, favorite_note_view

router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'tags', TagViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'sharedstatuses', SharedStatusViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = router.urls

urlpatterns += [
    path('comments/<pk>/reply/', comment_reply, name='comment_reply'),
    path('notes/<pk>/like/', like_note_view, name='like_note'),
    path('notes/<pk>/favorite/', favorite_note_view, name='favorite_note'),
]
