from multiprocessing import context
from rest_framework import serializers
from django.db.models import Avg
from django.contrib.auth import get_user_model
from datetime import date, timedelta

from .tasks import send_confirmation_code
from .utils import get_date

from .models import(
    Booking
)
User = get_user_model()


class  BookingCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    format = '%d.%m.%Y'

    def validate_created_at(self, created_at):
        if created_at.strptime(self.format) < date.today():
            raise serializers.ValidationError(
                'You cannot borrow in the past'
            )
        return created_at

    def validate_date_ended(self, created_at, date_ended, date_max_end):
        date_max_end = created_at.strptime(self.format) + timedelta(days=14)
        if date_ended.strptime(self.format) > date_max_end:
            raise serializers.ValidationError(
                'You cannot borrow books for more than 14 days.'
            )
        
    def perform_create(self, serializer): # для чего эта функция, чтобы не рописыать юзера в запрроме
        serializer.save(user=self.request.user)

    def create(self, validated_data):
        booking = Booking.objects.create_booking(**validated_data)
        booking.create_confirmation_code()
        send_confirmation_code.delay(booking.email, booking.confirmation_code)
        return booking

    class Meta:
        model = Booking
        fields = '__all__'


class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['rent_status', 'order_id', 'book']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['date_ended', 'date_max_end', 'rent_status']