from django.conf.urls import patterns, include, url
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail


class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail


urlpatterns = patterns('',
	url(r'^register/$', RegistrationViewUniqueEmail.as_view(), name='registration_register'),
	url(r'^', include('registration.backends.default.urls')),
	url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
    						    {'post_reset_redirect': '/accounts/password/reset/done/'}),
	url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
	url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
    							{'post_reset_redirect': '/accounts/password/done/'}),
	url(r'^password/done/$', 'django.contrib.auth.views.password_reset_complete'),
)
