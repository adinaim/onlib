from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
import hashlib
from datetime import datetime, timedelta

from .utils import get_date
from apps.book.models import Book

User = get_user_model()


class Booking(models.Model):
    TAKEN = 'TAKEN'
    RETURNED = 'RETURNED'
    OWES = 'OWES'

    RENT_STATUSES = (
        (TAKEN, 'Взял_а'),
        (RETURNED, 'Вернул_а'),
        (OWES, 'Должен_на')
    )
    
    order_id = models.CharField(max_length=8, primary_key=True)
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='order_book',
        null=True
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        related_name='order_user',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    rent_status = models.CharField(max_length=10, choices=RENT_STATUSES, default=TAKEN)
    created_at = models.DateTimeField(auto_now_add=True)#, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_ended = models.DateTimeField(default=datetime.now() + timedelta(days=14))
    date_max_end = models.DateTimeField(default=datetime.now() + timedelta(days=14))
    confirmation_code = models.CharField(max_length=16, blank=True)

#     room=models.ForeignKey(Room,on_delete=models.CASCADE)
#     guest=models.ForeignKey(Guest,on_delete=models.CASCADE)
#     hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
#     checkin_date=models.DateTimeField(default=datetime.now())
#     checkout_date=models.DateTimeField(default=datetime.now() + timedelta(days=1))
#     check_out=models.BooleanField(default=False)
#     no_of_guests=models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.order_id

    def save(self, *args, **kwargs):
        self.rent_status = self.TAKEN

    class Meta:
        ordering = ['created_at']  
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    # def _create(self, book, email, password, **extra_fields):
    #     if not username:
    #         raise ValueError('User must have username')
    #     if not email:
    #         raise ValueError('User must have email')
    #     booking = self.model(
    #         book=book,
    #         email=self.normalize_email(email),
    #         **extra_fields
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def create_booking(self, order_id, books, user, status, date_started, date_ended, date_max_end, **extra_fields):
        extra_fields.setdefault('rent_status', self.TAKEN)
        return 

    # def create_user(self, username, email, password, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_active', False)
    #     return self._create(username, email, password, **extra_fields)


    def create_confirmation_code(self):
        code = self.orders.email + str(self.order_id) + str(get_date())
        encode_string = code.encode()
        md5_object = str(hashlib.md5(encode_string))[:8]
        if User.objects.filter(confirmation_code=code).exists():
            self.create_confirmation_code()
        self.confirmation_code = md5_object
        self.save()


