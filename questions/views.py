# from django.shortcuts import render
# from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from . import models
from django.utils import timezone
from questions.forms import UserRegistrationForm, UserLoginForm, UserSettingsForm, AskForm, AnswerForm, UserForm

# from .models import Post 

# Create your views here.
		
def index(request):
    return render(request, 'new_questions.html', {
            'title': 'Вопросы',
            'questions': paginate(request, models.Question.objects.all()),
            'tags' : paginate(request, models.Tag.objects.hottest())[:10],
            'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
            'page_objects' : paginate(request, models.Question.objects.all()),
        })

def top(request):
    return render(request, 'new_questions.html', {
            'title': 'Топ вопросов',
            'questions': paginate(request, models.Question.objects.get_hot()),
            'tags' : paginate(request, models.Tag.objects.hottest())[:10],
            'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
            'page_objects' : paginate(request, models.Question.objects.get_hot()),
        })

def new(request):
    return render(request, 'new_questions.html', {
            'title': 'Новые',
            'questions': paginate(request, models.Question.objects.get_new()),
            'tags' : paginate(request, models.Tag.objects.hottest())[:10],
            'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
            'page_objects' : paginate(request, models.Question.objects.get_new()),
        })


def hot(request, id=1):
	"""docstring for Main_menu"""
	return render(request, "hot.html", {
		'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
		'tags' : paginate(request, models.Tag.objects.hottest())[:10],
		"questions" : paginate(request, objects_list = models.Question.objects.get_hot()),
		"page_objects" : paginate(request, objects_list = models.Question.objects.get_hot()),
		})
def profile(request, id):
	return render(request, "user_settings.html", {
		'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
		'tags' : paginate(request, models.Tag.objects.hottest())[:10],
		"profile": get_object_or_404(models.CustomUser, pk=id),
		})

def user_questions(request, id):	#Переделай вид страницы! не красиво!
	"""docstring for Main_menu"""
	return render(request, "user_question.html", {
		'questions': paginate(request, models.Question.objects.get_by_user(user_id=id)),
        'tags' : paginate(request, models.Tag.objects.hottest())[:10],
        'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
        'page_objects' : paginate(request, models.Question.objects.get_by_user(user_id=id)),
		})

def question_page(request, id):
	return render(request, "questions.html", {
		'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
		'tags' : paginate(request, models.Tag.objects.hottest())[:10],
		"question": get_object_or_404(models.Question, pk=id) ,
		"answers": paginate(request, objects_list = models.Answer.objects.get_hot_for_answer(id)),
		"page_objects": paginate(request, objects_list = models.Answer.objects.get_hot_for_answer(id)),
		})

def tag(request, id):
    return render(request, 'tag_find.html', {
        'users' : paginate(request, models.CustomUser.objects.by_rating())[0:10],
        'tags' : paginate(request, models.Tag.objects.hottest())[0:10],
        'tag' : get_object_or_404(models.Tag, pk=id) ,
        'questions': paginate(request, models.Question.objects.get_by_tag(tag_id=id)),
        "page_objects": paginate(request, objects_list = models.Question.objects.get_by_tag(tag_id=id)),
    })


def edit(request):
    user = get_object_or_404(models.CustomUser, username=request.user)

    if request.method == 'POST':
        form = UserSettingsForm(instance=user,
                               data=request.POST,
                               files=request.FILES
                              )
        if form.is_valid():
            form.save()
            return profile(request, user.id)
    else:
        form = UserSettingsForm(instance=user)

    return render(request, 'edit.html', {
            'form': form,
            'tags' : paginate(request, models.Tag.objects.hottest())[:10],
            'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
        })

@login_required(login_url='/log_in/')
def new_answer(request, id):
    if models.Question.objects.filter(id=id).exists():
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                #answeredQuestion = Question.objects.get_by_id(id)[0]
                answeredQuestion = get_object_or_404(models.Question, pk=id)
                answer = models.Answer.objects.create(author=request.user,
                                create_date=timezone.now(),
                                text=form.cleaned_data['text'],
                                question_id=answeredQuestion.id)
                answer.save()
                return redirect('/question/{}/add_answer/'.format(id))
        else:
            form = AnswerForm()
        #return render(request, 'question/new_answer.html', {'form': form})
        return render(request, 'questions.html', {
            'form': form,
            'question': get_object_or_404(models.Question, pk=id),
            'answers' : paginate(request, models.Answer.objects.get_hot_for_answer(id)),
            'tags' : paginate(request, models.Tag.objects.hottest())[:10],
            'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
            'page_objects' : paginate(request, models.Answer.objects.get_hot_for_answer(id)),
        })
    else:
        raise Http404

@login_required(login_url='/log_in/')
def ask(request):
    error = True
    if request.method == 'POST':
        firstly = False
        form = AskForm(request.POST)
        if form.is_valid():
            ques = models.Question.objects.create(author=request.user,
                            create_date=timezone.now(),
                            is_active=True,
                            title=form.cleaned_data['title'],
                            text=form.cleaned_data['text'])
            ques.save()

            for tagTitle in form.cleaned_data['tags'].split():
                tag = models.Tag.objects.get_or_create(title=tagTitle)[0]
                ques.tags.add(tag)
                ques.save()
            #return question(request, ques.id)
            return redirect('/question/{}/'.format(ques.id))
        else:
            error = False
    else:
        form = AskForm()
    firstly = True
    return render(request, 'new_ask.html', {
            'firstly': firstly,
            'error': error,
            'form': form,
            'tags' : paginate(request, models.Tag.objects.hottest())[:10],
            'users' : paginate(request, models.CustomUser.objects.by_rating())[:10],
        })

def signin(request):
    last_page = request.GET['next']
    if last_page == '/logout' or last_page == '/login':
        last_page = '/'
    error = False
    if request.method == 'POST':
        user = authenticate(username=request.POST['nickname'], password=request.POST['password'])
        if user is not None:
            login(request, user)  # Авторизуем пользователя
            return redirect(last_page)
        else:
            error = True
    return render(request, 'login.html',
                    {'error': error,
                    'last_page': last_page,
                    'tags' : paginate(request, models.Tag.objects.hottest()),
                    'users' : paginate(request, models.CustomUser.objects.by_rating()),
    })

def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, request.FILES)
        print(user_form)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect(request.GET.get('next') if request.GET.get('next') != '' else '/')
        else:
            print(user_form.errors)
    else:
        user_form = UserRegistrationForm()
    return render(request,'registration.html',
                          {'form':user_form,})

def signout(request):
    if not request.user.is_authenticated:
        raise Http404
    logout(request)
    #return redirect(request.GET['from'])
    return redirect('/')


def paginate(request, objects_list):
    paginator = Paginator(objects_list, 30)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects

@require_POST
def like_question(request):
    question_id = request.POST.get('question_id', '')
    like_type = request.POST.get('like_type', '')
    question =get_object_or_404(Question, pk=question_id)
    if not question:
        return JsonResponse({"status": "error"})

    if (like_type == 'like'):
        question.rating += 1
    elif (like_type == 'dislike'):
        question.rating -= 1
    question.save()

    return JsonResponse({"status": "ok"})

@require_POST
def like_answer(request):
    answer_id = request.POST.get('answer_id', '')
    like_type = request.POST.get('like_type', '')
    answer =get_object_or_404(Answer, pk=answer_id)
    if not answer:
        return JsonResponse({"status": "error"})

    if (like_type == 'like'):
        answer.rating += 1
    elif (like_type == 'dislike'):
        answer.rating -= 1
    answer.save()

    return JsonResponse({"status": "ok"})


@require_POST
def approve_answer(request):
    answer_id = request.POST.get('answer_id', '')
    answer =get_object_or_404(Answer, pk=answer_id)
    if not answer:
        return JsonResponse({"status": "error"})

    answer.approved = not answer.approved
    answer.save()

    return JsonResponse({"status": "ok"})