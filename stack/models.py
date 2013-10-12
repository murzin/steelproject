# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import utc
from datetime import datetime
from django.contrib.sites.models import Site


class Question(models.Model):
	caption = models.CharField(max_length=100)
	text = models.TextField()
	timestamp = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))
	author = models.ForeignKey(User)

	def get_absolute_url(self):
		return reverse('question_detail', kwargs={'pk': self.pk})

	def __unicode__(self):
		return self.caption


class Comment(models.Model):
	text = models.TextField()
	timestamp = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question, related_name='comments')

	def __unicode__(self):
		return self.author


@receiver(post_save, sender=Comment)
def send_new_comment_mail(sender, instance, **kwargs):
	message = u'Ваш вопрос:\n {0}\nТекст комментария:\n{1}\n{2}'.format(instance.question.text, instance.text,
											'http://' + Site.objects.all()[0].domain + reverse('question_detail', kwargs={'pk': instance.question.pk}))
	send_mail(u'Новый комментарий', message, "info@ex.com", [instance.question.author.email] )