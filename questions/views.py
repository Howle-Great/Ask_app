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

def hot(request, id):
	"""docstring for Main_menu"""
	return render(request, "hot.html", {
		'users' : paginate(request, User.objects.by_rating()),
		'tags' : paginate(request, Tag.objects.hottest())
		"questions": paginate(request, objects_list = models.Question.objects.get_hot()),
		"page_objects": paginate(request, objects_list = models.Question.objects.get_hot()),
		})
def profile(request, id):
	return render(request, "user_settings.html", {
		'users' : paginate(request, User.objects.by_rating()),
		'tags' : paginate(request, Tag.objects.hottest())
		"profile": get_object_or_404(models.CustomUser, pk=id),
		})

def user_questions(request, id):	#Переделай вид страницы! не красиво!
	"""docstring for Main_menu"""
	return render(request, "user_question.html", {
		'users' : paginate(request, User.objects.by_rating()),
		'tags' : paginate(request, Tag.objects.hottest())
		"questions": paginate(request, objects_list = models.Question.objects.get_by_user(id)),
		"page_objects": paginate(request, objects_list = models.Question.objects.get_hot()),
		})

def question_page(request, id):
	return render(request, "questions.html", {
		'users' : paginate(request, User.objects.by_rating()),
		'tags' : paginate(request, Tag.objects.hottest())
		"question": get_object_or_404(models.Question, pk=id) ,
		"answers": paginate(request, objects_list = models.Answer.objects.get_hot_for_answer(id)),
		"page_objects": paginate(request, objects_list = models.Answer.objects.get_hot_for_answer(id)),
		})

def tag(request, id):
    return render(request, 'question/tag_find.html', {
        'users' : paginate(request, User.objects.by_rating()),
        'tags' : paginate(request, Tag.objects.hottest()),
        'tag' : get_object_or_404(models.Tag, pk=id) ,
        'questions': paginate(request, Question.objects.get_by_tag(tag_id=id)),
        "page_objects": paginate(request, objects_list = models.Question.objects.get_by_tag(tag_id=id)),
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
    paginator = Paginator(objects_list, 10)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects