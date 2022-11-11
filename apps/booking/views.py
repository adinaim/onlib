from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.shortcuts import render
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from .permissions import IsOwner

# class AccountActivationView(APIView):
#     def get(self, request, activation_code): # зачем request, в методах APIView многие методы с реквестом, но он не используется, прочитать, почему
#         user = User.objects.filter(activation_code=activation_code).first()
#         if not user:
#             return Response(
#                 'Page not found.' ,
#                 status=status.HTTP_404_NOT_FOUND
#                 )
#         user.is_active = True
#         user.activation_code = ''
#         user.save()
#         return Response(
#             'Account activated. You can login now.',
#             status=status.HTTP_200_OK
#             ) 
# order_id = str(get_date()) + self.user.username


# @api_view(['GET','POST'])
# def api_booking_list_view(request):
#     booking=Booking.objects.all()
#     if request.method =='GET':
#         serializer=BookingListSerializer(booking,many=True)
#         return Response(serializer.data)
#     if request.methos=='POST':
#         serializer=BookingCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return BookingListSerializer
        elif self.action == 'create':
            return BookingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BookingUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == ['retrieve']:
            self.permission_classes = [IsOwner]
        if self.action == ['list']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(methods=['POST', 'PATCH', 'PUT'], detail=True, url_path='activate-booking')
    def confirm_booking(self, request, confirmation_code):
        booking = Booking.objects.filter(confirmation_code=confirmation_code).first()
        if not booking:
            return Response(
                'Page not found.' ,
                status=status.HTTP_404_NOT_FOUND
                )
        booking.rent_status = 'RENTED'
        booking.number_available -= 1
        booking.confirmation_code = ''
        booking.save()
        return Response(
            'Booking confirmed',
            status=status.HTTP_200_OK
            )



        


# class BookingActivationView(APIView):
#     def get(self, request, confirmation_code): 
#         booking = Booking.objects.filter(confirmation_code=confirmation_code).first()
#         if not booking:
#             return Response(
#                 'Page not found.' ,
#                 status=status.HTTP_404_NOT_FOUND
#                 )
#         booking.rent_status = RENTED
#         if booking.number_available >= 1
#         booking.number_available -= 1
#         booking.confirmation_code = ''
#         booking.save()
#         return Response(
#             'Booking confirmed.',
#             status=status.HTTP_200_OK
#             )