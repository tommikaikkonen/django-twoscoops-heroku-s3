from core.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django import forms

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email address already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
 
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
 
    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_username'])
 
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2
 
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeAdminForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': _("A user with that email address already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "is_active", "is_staff",
            "is_email_verified", "is_superuser", "groups", "user_permissions", "last_login", "date_joined")

    def __init__(self, *args, **kwargs):
        super(UserChangeAdminForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserChangeForm(forms.ModelForm):

    old_password = forms.CharField(label=_("Old password"),
        widget=forms.PasswordInput,
        help_text=_("If you want to change your password, fill out the remaining fields"),
        required=False)
    password1 = forms.CharField(label=_("New password"),
        widget=forms.PasswordInput,
        required=False)
    password2 = forms.CharField(label=_("New password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
        required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name",)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        old_password_valid = self.instance.check_password(old_password)

        if old_password_valid and password1 and password2:
            if old_password_valid and password1 == password2:
                self.cleaned_data['password'] = password2
            elif old_password_valid and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            elif not old_password_valid:
                raise forms.ValidationError("Old password is invalid")

        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

