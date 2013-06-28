from django.db import models

# Create your models here.

import hashlib
import random

from registration.models import RegistrationProfile, RegistrationManager
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ugettext as _

class EmailRegistrationManager(RegistrationManager):
    def create_profile(self, user):
        """
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.
        
        The activation key for the ``RegistrationProfile`` will be a
        SHA1 hash, generated from a combination of the ``User``'s
        username and a random salt.
        
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.email
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt+username).hexdigest()
        return self.create(user=user,
                           activation_key=activation_key)

    def create_inactive_user(self, email, password, site, send_email=True, **kwargs):
        """
        Create a new, inactive ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, an activation email will be sent to the new
        user. To disable this, pass ``send_email=False``.
        
        """
        user = get_user_model()
        print user
        new_user = user.objects.create_user(email, password, **kwargs)
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user)

        if send_email:
            registration_profile.send_activation_email(site)

        return new_user

class EmailRegistrationProfile(RegistrationProfile):
    objects = EmailRegistrationManager()