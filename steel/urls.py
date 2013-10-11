from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/', include('steel.registration_urls')),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},
																						name='auth_login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),
	url(r'', include('social_auth.urls')),
	url(r'^', include('stack.urls')),
)
