# Create your views here.

from django.views.generic import DetailView
from django.views.generic.edit import FormView
from core.models import User
from core.forms import UserChangeForm
from braces.views import LoginRequiredMixin

class UserDetailView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserDetailView, self).get_context_data(**kwargs)
        return context

class UserUpdateView(LoginRequiredMixin, FormView):
    form_class = UserChangeForm
    template_name = "core/user_update.html"

    def get_form_kwargs(self, **kwargs):
        kwargs = super(UserUpdateView, self).get_form_kwargs(**kwargs)
        kwargs['instance'] = User.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super(UserUpdateView, self).form_valid(form)