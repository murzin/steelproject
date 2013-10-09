from django.conf.urls import patterns, include, url
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail


class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail


urlpatterns = patterns('',
	url(r'^register/$', RegistrationViewUniqueEmail.as_view(), name='registration_register'),
	url(r'^', include('registration.backends.default.urls')),
)
