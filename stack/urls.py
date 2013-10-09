from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView
from models import Question

urlpatterns = patterns('',
	url(r'^$', ListView.as_view(template_name='index.html', model=Question), name='index'),
	url(r'^take_question/$', TakeQuestion, name='take_question'),
)
