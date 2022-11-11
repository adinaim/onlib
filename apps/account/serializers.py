from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
# from dateutil.relativedelta import relativedelta

from .tasks import send_activation_code
from .models import UserProfile#, UserImage


User = get_user_model()

def email_validator(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with such email is not found.'
            )
        return email


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate_username(self, username):
        user = self.context.get('request').user
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'The username is already in use. Choose another one.'
                )
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        if len(username) < 5 or len(username) > 16:
            raise serializers.ValidationError('Username must be between 5 and 16 characters long.')
        if not username.replace('_', '').replace('.', '').isalnum(): 
            raise serializers.ValidationError('Username can only contain letters, numbers, an \'_\' and \'.\'.')
        if '_.' in username or '._' in username:
            raise serializers.ValidationError('\'_\' and \'.\' cannot stand next to each other.')
        if not username[0].isalpha():
            raise serializers.ValidationError('Username must start with a letter.')
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'The email is already in use.'
                )
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают.')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code.delay(user.email, user.activation_code)
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
    new_pass_confirm = serializers.CharField(max_length=128, required=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                'Неверный пароль.'
            )
        return old_password

    def validate(self, attrs: dict):
        new_password = attrs.get('new_password')
        new_pass_confirm = attrs.get('new_pass_confirm')
        if new_password != new_pass_confirm:
            raise serializers.ValidationError(
                'Passwords do not match.'
            )
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255, 
        required=True, 
        validators=[email_validator]
        )

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            subject='Password restoration',
            message=f'Your code for password restoration {user.activation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255, 
        required=True,
        validators=[email_validator]
        )
    code = serializers.CharField(min_length=1, max_length=8, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
    new_password_confirm = serializers.CharField(max_length=128, required=True)

    def validate_code(self,code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError(
                'Wrong code.'
            )
        return code

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                'Passwords do not match.'
            )
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.activation_code = ''
        user.save()


class UserProfileCreateSerializer(serializers.Serializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=40)
    bio = serializers.CharField(max_length=5000)
    avatar = serializers.ImageField()   #######
    birthday = serializers.DateField()                         # settings include format   # формат как проверяется, выпдает ли календарь
    phone = serializers.CharField(max_length=14) 

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['image'] = UserAvatarSerializer(
    #         instance.avatar.all()
    #     ).data   

    class Meta:
        model = UserProfile
        fields = ('__all__')


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

# class UserAvatarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserImage
#         fields = 'image'