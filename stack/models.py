from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
	caption = models.CharField(max_length=100)
	text = models.TextField()
	timestamp = models.DateTimeField()
	author = models.ForeignKey(User)

	def get_absolute_url(self):
		return reverse('question_detail', kwargs={'pk': self.pk})

	def __unicode__(self):
		return self.caption


class Comment(models.Model):
	text = models.TextField()
	timestamp = models.DateTimeField()
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question, related_name='comments')

	def __unicode__(self):
		return self.author
