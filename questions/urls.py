from django.contrib import admin
from django.urls import path
from questions import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.TagPage.as_view(), name="tag"),
	path('new_questions', views.NewQuestions.as_view(), name="question"),
	path('questions', views.Questions.as_view(), name="questions"),
	path('sign_up', views.Registration.as_view(), name="registr"),
	path('settings', views.Settings.as_view(), name="setting"),
	path('new_ask', views.NewAsk.as_view(), name="ask"),

	# In working
	path('user/<int:id>/', views.profile, name="user"),
	path('user/questions/<int:id>/', views.user_questions, name='user_questions'),
	path('question_page/<int:id>', views.question_page, name='question_page'),
	path('question/<int:id>/add_answer/', views.new_answer, name='new_answer'),
	path('ask/', views.ask, name='ask'),
	path('log_in/', views.signin, name="login"),
	path('tag/<int:id>', views.tag, name='tag'),
	path('hot/<int:id>/', views.hot, name="hot"),
	path('registration/', views.registration, name='registration'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




