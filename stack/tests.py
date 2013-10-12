# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.core import mail
import re
from django.contrib.auth.models import User
from models import Question, Comment
from django.contrib.sites.models import Site


class SimpleTest(TestCase):
	def setUp(self):
		self.site = Site.objects.all()[0]
		self.site.domain = 'localhost:8000'
		self.site.save()
		self.u1 = User.objects.create_user(username='user1', email='u1@mail.com', password='password')
		self.u2 = User.objects.create_user(username='user2', email='u2@mail.com', password='password')
		self.question1 = Question.objects.create(caption='Caption1', text='text1', author=self.u1)
		self.question2 = Question.objects.create(caption='Caption2', text='text2', author=self.u2)
		self.comment11 = Comment.objects.create(text='text11', author=self.u2, question=self.question1)
		self.comment12 = Comment.objects.create(text='text12', author=self.u2, question=self.question1)
		self.comment21 = Comment.objects.create(text='text21', author=self.u1, question=self.question2)
		self.comment22 = Comment.objects.create(text='text22', author=self.u1, question=self.question2)

	def test_index_menu(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'главную')

	def test_index_no_login(self):
		response = self.client.get(reverse('index'))
		for question in Question.objects.all():
			self.assertContains(response, question.caption)

	def test_user_regisrtration(self):
		response = self.client.post(reverse('registration_register'),
						 {'username': 'testuser', 'email': 'email@test.com', 'password1': 'pass', 'password2': 'pass'},
						 follow=True,
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, u'На ваш e-mail отправлен код подтверждения.')
		self.assertEqual(u'Активация аккаунта' in mail.outbox[-1].subject, True)
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mail.outbox[-1].body)
		response = self.client.get(urls[0], follow=True)
		self.assertContains(response, u'Ваша учетная запись активирована.')

	def test_login_form(self):
		response = self.client.post(reverse('auth_login'),
						 {'username': 'user1', 'password': 'password'},
						 follow=True,
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.client.session['_auth_user_id'], User.objects.get(username='user1').pk)

	def test_question_detail_no_login(self):
		response = self.client.get(reverse('question_detail', kwargs={'pk': self.question1.pk}))
		self.assertContains(response, self.question1.caption)
		for comment in self.question1.comments.all():
			self.assertContains(response, comment.text)
		self.assertContains(response, u'Оставить комментарий могут только зарегистрированные пользователи')
		self.assertNotContains(response, '<form method="post" action="">')

	def test_question_add_login(self):
		self.client.login(username='user1', password='password')
		response = self.client.post(reverse('question_add'),
			{'caption': u'Тестовый кэпшн', 'text': u'Тестовый текст'}, follow=True,
		)
		self.assertContains(response, u'Тестовый текст')
		self.assertEqual(len(Question.objects.filter(caption=u'Тестовый кэпшн')),1)

	def test_question_detail_login(self):
		self.client.login(username='user1', password='password')
		response = self.client.get(reverse('question_detail', kwargs={'pk': self.question1.pk}))
		self.assertContains(response, self.question1.caption)
		for comment in self.question1.comments.all():
			self.assertContains(response, comment.text)
		self.assertContains(response, '<form method="post" action="">')

	def test_question_comment_login(self):
		self.client.login(username='user1', password='password')
		response = self.client.post(reverse('question_detail', kwargs={'pk': self.question1.pk}),
			{'text': u'Тестовый текст'}, follow=True,
		)
		self.assertContains(response, u'Тестовый текст')
		self.assertEqual(len(Comment.objects.filter(text=u'Тестовый текст')),1)
		''' Signal test'''
		self.assertEqual(u'Тестовый текст' in mail.outbox[-1].body, True)

	def test_password_reset(self):
		response = self.client.post(reverse('auth_password_reset'), {'email': self.u2.email}, follow=True)
		self.assertContains(response, u'Инуструкции по смене пароля высланы в письме')
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mail.outbox[-1].body)
		response = self.client.post(urls[0], {'new_password1': '1', 'new_password2': '1'}, follow=True)
		self.assertContains(response, u'Пароль изменен')
		self.client.login(username='user2', password='1')
		self.assertEqual(self.client.session['_auth_user_id'], self.u2.pk)

	def test_logout(self):
		self.client.login(username='user1', password='password')
		self.client.get(reverse('auth_logout'))
		self.assertNotIn('_auth_user_id', self.client.session)









