from django.views.generic import DetailView
from django.views.generic.edit import CreateView, ProcessFormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
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
		print 'form valid question pk = ' + self.kwargs['pk']
		return super(QuestionDetail, self).form_valid(form)


	def get_context_data(self, **kwargs):
		context = super(QuestionDetail, self).get_context_data(**kwargs)
		context['question'] = get_object_or_404(Question, pk=self.kwargs['pk'])
		print 'context question pk = ' + self.kwargs['pk']
		return context

	def get_success_url(self):
		return reverse_lazy('question_detail', kwargs={'pk': self.kwargs['pk']})

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		self.question = get_object_or_404(Question, pk=self.kwargs['pk'])
		return super(QuestionDetail, self).dispatch(*args, **kwargs)






#
#
#class QuestionDetail1(DetailView, ProcessFormView):
#	model = Question
#	template_name = 'question_detail.html'
#	form_class = CommentForm
#
#	def get_context_data(self, **kwargs):
#		context = super(QuestionDetail, self).get_context_data(**kwargs)
#		context['form'] = CommentForm()
#		return context







#class TakeQuestion(FormView):
#	template_name = 'take_question.html'
#	form_class = QuestionForm
#	success_url = '/'
#
#	def form_valid(self, form):
#		return super(TakeQuestion, self).form_valid(form)