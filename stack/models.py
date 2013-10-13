# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.timezone import utc
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
	caption = models.CharField(max_length=100, verbose_name=_(u"Тема"))
	text = models.TextField(verbose_name=_(u"Текст"))
	timestamp = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc), verbose_name=_(u"Время"))
	author = models.ForeignKey(User, verbose_name=_(u"Автор"))

	def get_absolute_url(self):
		return reverse('question_detail', kwargs={'pk': self.pk})

	def __unicode__(self):
		return self.caption

	class Meta:
		verbose_name = _(u"Вопрос")
		verbose_name_plural = _(u"Вопросы")


class Comment(models.Model):
	text = models.TextField(verbose_name=_(u"Текст комментария"))
	timestamp = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question, related_name='comments')

	def __unicode__(self):
		return self.author

	class Meta:
		verbose_name = _(u"Комментарий")
		verbose_name_plural = _(u"Комментарии")


@receiver(post_save, sender=Comment)
def send_new_comment_mail(sender, instance, **kwargs):
	message = u'Ваш вопрос:\n {0}\nТекст комментария:\n{1}\n{2}'.format(instance.question.text, instance.text,
											'http://' + Site.objects.all()[0].domain + reverse('question_detail', kwargs={'pk': instance.question.pk}))
	send_mail(u'Новый комментарий', message, "info@ex.com", [instance.question.author.email] )