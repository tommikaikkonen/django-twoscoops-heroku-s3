from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.mail import send_mail
from django_extensions.db.fields import UUIDField

# Create your models here.

class EmailUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email address must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, first_name=u"Admin", last_name=u"User", **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    uuid = UUIDField(unique=True, auto=True)
    
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_email_verified = models.BooleanField('verified', default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
 
    USERNAME_FIELD = 'email'
 
    objects = EmailUserManager()
 
    def get_full_name(self):
      return u' '.join((self.first_name, self.last_name))
    
    def get_short_name():
      return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

