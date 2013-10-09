from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
	caption = models.CharField(max_length=100)
	text = models.TextField()
	timestamp = models.DateTimeField()
	author = models.ForeignKey(User)


class Comment(models.Model):
	text = models.TextField()
	timestamp = models.DateTimeField()
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question)
