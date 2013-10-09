from django.forms import ModelForm
from models import *


class QuestionForm(ModelForm):
	class Meta:
		model = Question


class CommentForm(ModelForm):
	class Meta:
		model = Comment
