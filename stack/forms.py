from django.forms import ModelForm
from models import *
from django import forms

class QuestionForm(ModelForm):
	class Meta:
		model = Question
		exclude = ('author', 'timestamp',)
		widgets = {
			"caption": forms.TextInput(attrs={'class': 'form-control'}),
			"text": forms.Textarea(attrs={'class': 'form-control'})
		}


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('author', 'timestamp', 'question')
		widgets = {
			"text": forms.Textarea(attrs={'class': 'form-control'})
		}
