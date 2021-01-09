# Import Python Package
from django.db import models
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create Auth User accroding to Developer Code
class UserManager(BaseUserManager):

    use_in_migrations = True

    # function for crate user or super user
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # function for add normal user's other field
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    # function for add super user's other field
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # display error message if is_staff and is_superuser is false for superuser.
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')
        return self._create_user(email, password, **extra_fields)


# Create Auth User Model Start
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(ugettext_lazy('Email Address'), unique=True)
    full_name = models.CharField(ugettext_lazy('Full Name'), max_length=50, blank=True, null=True, db_column="full_name")
    user_image = models.ImageField(ugettext_lazy('Profile Image'), blank=True, null=True, db_column="user_image", upload_to='user/profile/')
    device_token = models.CharField(ugettext_lazy('Device Token'), max_length=50, blank=True, null=True, db_column="device_token")
    about_me = models.TextField(ugettext_lazy('About Me'), blank=True, null=True, db_column="about_me")
    location = models.TextField(ugettext_lazy('Location'), blank=True, null=True, db_column="location")
    address = models.TextField(ugettext_lazy('Address'), blank=True, null=True, db_column="address")
    zip_code = models.BigIntegerField(ugettext_lazy('Zip Code'), blank=True, null=True, db_column="zip_code")
    latitude = models.BigIntegerField(ugettext_lazy('Latitude'), blank=True, null=True, db_column="latitude")
    longitude = models.BigIntegerField(ugettext_lazy('Longitude'), blank=True, null=True, db_column="longitude")
    distance = models.IntegerField(ugettext_lazy('Distance'), blank=True, null=True,  db_column="distance")
    otp = models.IntegerField(ugettext_lazy('OTP'), blank=True, null=True,  db_column="otp")
    update_by = models.IntegerField(ugettext_lazy('Update By'), blank=True, null=True,  db_column="update_by")
    update_dt = models.IntegerField(ugettext_lazy('Update Dt'), blank=True, null=True,  db_column="update_dt")

    USERNAME_FIELD = 'email'  # set email as a username
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "User Info"  # display table name for admin
        db_table = 'User_Info'  # display table name for admin