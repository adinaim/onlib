from multiprocessing import context
from rest_framework import serializers
from django.db.models import Avg

from .models import(
    Author,
    Book,
    Genre,
    Comment,
    Rating,
    Like
)



class BookListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(
        source='author.name'
    )

    class Meta:
        model = Book
        fields = ['author', 'title', 'genre', 'image_link', 'slug']


# class CurrentAuthorDefault:
#     requires_context = True

#     def __call__(self, serializer_field):
#         return serializer_field.context['request'].author

#     def __repr__(self):
#         return '%s()' % self.__class__.__name__


class BookCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=5000)
    image_link = serializers.CharField(max_length=255)
    year = serializers.IntegerField()   #
    pages = serializers.IntegerField()  #
    number_of_copies = serializers.IntegerField()
    number_available = serializers.IntegerField()

    def validate(self, attrs):
        title = attrs.get('title')
        if Book.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                'Such book already exists.'
            ) 
        return attrs
 
    def create(self, validated_data):
        genre = validated_data.pop('genre')
        book = Book.objects.create(**validated_data)
        book.genre.set(genre)
        return book

    class Meta:
        model = Book
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(
        source='author.name'
    )

    class Meta:
        model = Book
        fields = '__all__'


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'slug']


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'books__title']

    def to_representation(self, instance: Author):
        books = instance.books.all()
        representation = super().to_representation(instance)  
        representation['books'] = BookListSerializer(
            instance=books, many=True).data
        return representation


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    about = serializers.CharField(max_length=5000, required=True)
    avatar = serializers.CharField(max_length=250, required=True)
    name = str(first_name) + ' ' + str(last_name)

    def validate(self, attrs):
        author = attrs.get('name')
        if Author.objects.filter(name=author).exists():
            raise serializers.ValidationError(
                'Such author already exists.'
            ) 
        return attrs

    class Meta:
        model = Author
        fields = ('__all__')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

        def validate(self, attrs):
            genre = attrs.get('genre')
            if Genre.objects.filter(genre=genre).exists():
                raise serializers.ValidationError(
                    'Such genre already exists.'
                ) 
            return attrs


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre']


class GenreRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['slug']

    def to_representation(self, instance: Genre):
        books = instance.books.all()
        representation = super().to_representation(instance)  
        representation['books'] = BookListSerializer(
            instance=books, many=True).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )

    class Meta:
        model = Rating
        fields = ('rating', 'user', 'book')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating')
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError(
                'Wrong value! Rating should be between 1 and 5.'
                )
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class CurrentBookDefault:    # для чего
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['book']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    book = serializers.HiddenField(default=CurrentBookDefault())

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        book = self.context.get('book').pk
        like = Like.objects.filter(user=user, book=book).first()
        if like:
            raise serializers.ValidationError('Book has been liked.')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        book = self.context.get('book').pk
        like = Like.objects.filter(user=user, book=book).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('Not liked yet')


class FavoriteBookSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.URLField(source='book.get_absolute_url')
    book = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Like
        fields = ['book', 'user', 'url']