from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from slugify import slugify


User = get_user_model()


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    about = models.TextField()
    avatar = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=120)
    name = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.first_name) + '_' + slugify(self.last_name)
        if not self.name:
            self.name = str(self.first_name) + ' ' + str(self.last_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
    

class Book(models.Model):  
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, primary_key=True, blank=True)
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='books_author'
    )
    description = models.TextField(blank=True)
    image_link = models.CharField(max_length=255, blank=True)
    genre = models.ManyToManyField(
        to='Genre',
        related_name='books_genre',
        blank=True
    )
    year = models.PositiveSmallIntegerField(blank=True)   #
    pages = models.PositiveSmallIntegerField(blank=True)   #
    number_of_copies = models.PositiveSmallIntegerField()
    number_available = models.PositiveSmallIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.is_available = self.number_available > 0
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})     # вспомнить для чего

    class Meta:
        ordering = ['title']  
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Genre(models.Model):                                       
    genre = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=35)

    def __str__(self) -> str:
        return self.genre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genre)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.user.username} to {self.book.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Rating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE =5
    RATING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    def __str__(self) -> str:
        return str(self.rating)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Like(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='book_likes'
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='book_likes'
    )

    def __str__(self):
        return f'Liked by {self.user.username}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'











# first_name = response.css('div.dey4wx-1.jVKkXg::text').get().replace('&nbsp;', ' ').split()[0]
        # last_name = response.css('div.dey4wx-1.jVKkXg::text').get().replace('&nbsp;', ' ').split()[1]
        # avatar = response.xpath('//div/picture/source/@srcset').get().split(',')[0]   
        # bio = response.css('div.iszfik-2.gAFRve p::text').get() 
        # name = first_name + ' ' + last_name
        # slug = slugify(name)


        # author = { 
        #     'first_name': first_name,
        #     'last_name': last_name,
        #     'avatar': avatar,
        #     'bio': bio,
        #     'name': name, 
        #     'slug': slug
        # }

        # return author




#  'number_of_copies': random.randint(1, 10),




        # title = response.css('h1.sc-bdfBwQ.lnjchu-0.jzwvLi.gUKDCi.sc-1c0xbiw-11.bzVsYa::text').get().replace('&nbsp;', ' ')
        # slug = slugify(title)
        # image_link = response.xpath('//div/picture/source/@srcset').get().split(',')[0]    
        # description = response.css('div.iszfik-2.gAFRve p::text').get() 
        # genres = response.css('div.sc-1sg8rha-0.gHinNz div a::text').extract()
        # author = 
        # year = 
        # pages = 
        # number_of_copies=
        # genre = []
        # for topic in genres:
        #     topic.capitalize()
        #     genre.append(topic)