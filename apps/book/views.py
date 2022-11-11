from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import mixins, status, filters
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as rest_filter
from rest_framework.generics import ListAPIView

from .permissions import IsOwner

from .models import (
    Author,
    Book,
    Genre,
    Comment,
    Rating,
    Like
    )

from .serializers import (
    AuthorSerializer,
    AuthorListSerializer,
    AuthorCreateSerializer,
    AuthorRetrieveSerializer,

    BookSerializer,
    BookCreateSerializer,
    BookListSerializer,

    GenreSerializer,
    GenreListSerializer,
    GenreRetrieveSerializer,

    CommentSerializer,
    FavoriteBookSerializer,
    LikeSerializer,  
    RatingSerializer
    )


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend, 
        filters.OrderingFilter
        ]
    search_fields = ['name'] 
    filterset_fields = ['name']
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorListSerializer
        elif self.action == 'create':
            return AuthorCreateSerializer
        # elif self.action == 'retrieve':
        #     return AuthorRetrieveSerializer
        return super().get_serializer_class() 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'comment' and self.request.method == 'DELETE':
            self.permission_classes = [IsOwner, IsAdminUser]
        if self.action in ['create', 'comment', 'set_rating', 'like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions() 
    
    def retrieve(self, request: Request, title: str = None):
        if title:
            retrieve_category = get_object_or_404(Author, title=title)
            serializer = AuthorRetrieveSerializer(instance=retrieve_category)
        else:
            categories = Author.objects.all()
            serializer = AuthorRetrieveSerializer(instance=categories, many=True)
    

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend, 
        filters.OrderingFilter
        ]
    search_fields = ['title', 'author__name'] 
    filterset_fields = ['genre__genre']
    ordering_fields = ['created_at', 'title', 'author__name']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        elif self.action == 'create':
            return BookCreateSerializer
        return super().get_serializer_class() 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions() 

    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request, pk=None):
        book = self.get_object() 
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, book=book)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )      

    @action(methods=['POST', 'PATCH'], detail=True, url_path='set-rating')
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['book'] = pk                                                      
        serializer = RatingSerializer(data=data, context={'request': request})
        rate = Rating.objects.filter(
            user=request.user,
            book=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if rate and request.method == 'POST':
                return Response(
                    {'detail': 'Rating object exists. Use PATCH method'}
                )
            elif rate and request.method =='PATCH':
                serializer.update(rate, serializer.validated_data)
                return Response('Updated')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            return Response({'detail': 'Rating object does not exist. Use POST method'})

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        book = self.get_object()
        serializer = LikeSerializer(data=request.data, context={
            'request': request, 
            'book': book
            })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Liked!')
            if request.method == "DELETE":
                serializer.unlike()
                return Response('Unliked!')

    
class CommentCreateDeleteView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]


class FavoriteBookView(ListAPIView):
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)

   
class GenreViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return GenreListSerializer
        # elif self.action == 'retrieve':
        #     return GenreRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['destroy', 'create']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def retrieve(self, request: Request, title: str = None):
        if title:
            retrieve_category = get_object_or_404(Genre, title=title)
            serializer = GenreRetrieveSerializer(instance=retrieve_category)
        else:
            categories = Genre.objects.all()
            serializer = GenreRetrieveSerializer(instance=categories, many=True)