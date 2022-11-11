from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
import hashlib


class UserManager(BaseUserManager):

    def _create(self, username, password, email, **extra_fields):
        if not username:
            raise ValueError('User must have username')
        if not email:
            raise ValueError('User must have email')
      
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        return self._create(username, password, email, **extra_fields)

    def create_superuser(self, username, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(username, password, email, **extra_fields)


class User(AbstractBaseUser):

    username = models.CharField('username', max_length=16, primary_key=True)
    email = models.EmailField('email', max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self) -> str:
        return self.username

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = self.email + str(self.id)
        encode_string = code.encode()
        md5_object = hashlib.md5(encode_string)
        # code = get_random_string(length=8)
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = md5_object
        self.save()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserProfile(models.Model):
    user = models.OneToOneField(        # user или username
        to=User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    first_name = models.CharField('first name', max_length=20)
    last_name = models.CharField('last name', max_length=40)
    bio = models.TextField(default='', blank=True)
    avatar = models.ImageField(upload_to='media')#upload_to='media')    #######
    birthday = models.DateField(null=True, blank=True)                         # settings include format   # формат как проверяется, выпдает ли календарь
    phone = models.CharField(max_length=14, null=True)    # проверка на номер телефона
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' 

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


# class UserImage(models.Model):
#     image = models.ImageField() ######
#     user = models.ForeignKey(
#         to=UserProfile,
#         on_delete=models.CASCADE,
#         related_name='user_images'
#     )