# from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from . import models

# from .models import Post 

# Create your views here.
class TagPage(TemplateView):
	# model = Post
	template_name = "tag_find.html"

class NewQuestions(TemplateView):
	"""docstring for Questions"""
	template_name = "new_questions.html"
		
# class Hot(TemplateView):
# 	"""docstring for Hot"""
# 	template_name = "hot.html"

def hot(request, page=1):
	"""docstring for Main_menu"""
	return render(request, "hot.html", {
		"questions": paginate(request, objects_list = models.Question.objects.get_hot()),
		})

class Questions(TemplateView):
	"""docstring for Hot"""
	template_name = "questions.html"

class Registration(TemplateView):
	"""docstring for Hot"""
	template_name = "registration.html"

class Settings(TemplateView):
	"""docstring for Hot"""
	template_name = "settings.html"

class Login(TemplateView):
	"""docstring for Hot"""
	template_name = "login.html"

class NewAsk(TemplateView):
	"""docstring for Hot"""
	template_name = "new_ask.html"


def paginate(request, objects_list):
    paginator = Paginator(objects_list, 4)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects