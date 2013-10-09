from django.contrib import admin
from models import *


class CommentInline(admin.StackedInline):
	model = Comment


class QuestionAdmin(admin.ModelAdmin):
	inlines = [CommentInline]
	extra = 1


admin.site.register(Question, QuestionAdmin)