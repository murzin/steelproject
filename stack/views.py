from django.views.generic import TemplateView


class TakeQuestion(TemplateView):
	template_name = 'take_question.html'