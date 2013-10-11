from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from datetime import datetime
from models import Question, Comment
from forms import QuestionForm, CommentForm


class QuestionCreate(CreateView):
	model = Question
	form_class = QuestionForm
	template_name = 'question_add.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.timestamp = datetime.now()
		return super(QuestionCreate, self).form_valid(form)

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(QuestionCreate, self).dispatch(*args, **kwargs)


class QuestionDetail(CreateView):
	model = Comment
	form_class = CommentForm
	template_name = 'question_detail.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.timestamp = datetime.now()
		form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
		return super(QuestionDetail, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(QuestionDetail, self).get_context_data(**kwargs)
		context['question'] = get_object_or_404(Question, pk=self.kwargs['pk'])
		return context

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		return super(CreateView, self).post(self, request, *args, **kwargs)

	def get_success_url(self):
		return reverse('question_detail', kwargs={'pk': self.kwargs['pk']})

	def dispatch(self, *args, **kwargs):
		return super(QuestionDetail, self).dispatch(*args, **kwargs)


