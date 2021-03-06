from django.conf.urls import patterns, url
from django.views.generic import ListView
from views import QuestionCreate, QuestionDetail
from models import Question

urlpatterns = patterns('',
	url(r'^$', ListView.as_view(template_name='index.html', model=Question), name='index'),
	url(r'^question/add/$', QuestionCreate.as_view(), name='question_add'),
	url(r'^question/(?P<pk>\d+)/$', QuestionDetail.as_view(), name='question_detail'),
)
