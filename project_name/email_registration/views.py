# Create your views here.

# Create your views here.
from django.contrib.sites.models import Site, RequestSite

from registration.views import RegistrationView
from registration import signals
from core.forms import UserCreationForm
from email_registration.models import EmailRegistrationProfile

class EmailRegistrationView(RegistrationView):
    form_class = UserCreationForm
    success_url = "/"

    def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        email, password = cleaned_data['email'], cleaned_data['password1']
        first_name, last_name = cleaned_data['first_name'], cleaned_data['last_name']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = EmailRegistrationProfile.objects.create_inactive_user(email,
                                                                    password, site,
                                                                    first_name=first_name,
                                                                    last_name=last_name)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user