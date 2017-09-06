from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from care.constants import DOCTOR_CLASSIFY
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class UserManager(BaseUserManager):
    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('手机号不能为空')

        user = self.model(phone=phone,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given phone, date of
        birth and password.
        """
        extra_fields.setdefault('is_admin', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """
        Creates and saves a superuser with the given phone, date of
        birth and password.
        """
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)

SEX = (
    ('male', '男'),
    ('female', '女'),
    ('secret', '保密'),
)

TYPE = (
    ('player', '玩家'),
    ('normal', '用户'),
    ('doctor', '医生')
)

class User(AbstractBaseUser):
    phone = models.CharField(
        verbose_name='phone address',
        max_length=11,
        unique=True,
    )
    user_type = models.CharField(choices=TYPE, max_length=6, blank=True)
    name = models.CharField(max_length=10, blank=True)
    sex = models.CharField(choices=SEX, max_length=6, blank=True)
    team = models.CharField('所属医院或战队', max_length=255, default=None, blank=True, null=True)
    game = models.CharField(max_length=140, default=None, null=True, blank=True)
    job = models.CharField('职位', max_length=140, default=None, null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['sex', 'team', 'job', 'email']

    def get_full_name(self):
        # The user is identified by their phone address
        return self.phone

    def get_short_name(self):
        # The user is identified by their phone address
        return self.name

    def __str__(self):              # __unicode__ on Python 2
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='doctor_image', null=True, blank=True)
    classify = models.CharField('医生类别', max_length=30, blank=True, choices=DOCTOR_CLASSIFY)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created and instance.user_type == 'doctor':
            DoctorProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            pass

    @property
    def user__phone(self):
        return self.user.phone
