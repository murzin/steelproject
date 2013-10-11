# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.core import mail
import re
from django.contrib.auth.models import User
from models import Question, Comment
from datetime import datetime

class SimpleTest(TestCase):
	def setUp(self):
		self.u1 = User.objects.create_user(username='user1', email='u1@mail.com', password='password')
		self.u2 = User.objects.create_user(username='user2', email='u2@mail.com', password='password')
		self.question1 = Question.objects.create(caption='Caption1', text='text1', timestamp=datetime.now(), author=self.u1)
		self.question2 = Question.objects.create(caption='Caption2', text='text2', timestamp=datetime.now(), author=self.u2)
		self.comment11 = Comment.objects.create(text='text11', timestamp=datetime.now(), author=self.u2, question=self.question1)
		self.comment12 = Comment.objects.create(text='text12', timestamp=datetime.now(), author=self.u2, question=self.question1)
		self.comment21 = Comment.objects.create(text='text21', timestamp=datetime.now(), author=self.u1, question=self.question2)
		self.comment22 = Comment.objects.create(text='text22', timestamp=datetime.now(), author=self.u1, question=self.question2)

	def test_main_page(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'главную')

	def test_user_regisrtration(self):
		response = self.client.post(reverse('registration_register'),
						 {'username': 'testuser', 'email': 'email@test.com', 'password1': 'pass', 'password2': 'pass'},
						 follow=True,
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, u'На ваш e-mail отправлен код подтверждения.')
		self.assertEqual(len(mail.outbox), 5)
		self.assertEqual(mail.outbox[4].subject, u'Активация аккаунта – example.com')
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mail.outbox[4].body)
		response = self.client.get(urls[0], follow=True)
		self.assertContains(response, u'Ваша учетная запись активирована.')

	def test_login(self):
		response = self.client.post(reverse('auth_login'),
						 {'username': 'user1', 'password': 'password'},
						 follow=True,
		)
		self.assertEqual(response.status_code, 200)
		#import pdb
		#pdb.set_trace()
		self.assertEqual(self.client.session['_auth_user_id'], User.objects.get(username='user1').pk)

	def test_index_no_login(self):
		response = self.client.get(reverse('index'))
		self.assertContains(response, 'Caption1')




