from django.forms import ModelForm
from models import *


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		exclude = ('author', 'timestamp',)


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('author', 'timestamp', 'question')
