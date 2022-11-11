from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthorViewSet,
    BookViewSet,
    GenreViewSet,
    CommentCreateDeleteView,
    FavoriteBookView
    )


router = DefaultRouter()
router.register('author', AuthorViewSet)
router.register('book', BookViewSet)
router.register('genre', GenreViewSet)
router.register('comment', CommentCreateDeleteView, 'comment')

urlpatterns = [
    path('liked/', FavoriteBookView.as_view(), name='liked')
]

urlpatterns += router.urls
