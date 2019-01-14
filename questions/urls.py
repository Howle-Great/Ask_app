from django.urls import path

from . import views

urlpatterns = [
	path('', views.TagPage.as_view(), name="tag"),
	path('new_questions', views.NewQuestions.as_view(), name="question"),
	path('hot/<int:page>/', views.hot, name="hot"),
	path('questions', views.Questions.as_view(), name="questions"),
	path('sign_up', views.Registration.as_view(), name="registr"),
	path('settings', views.Settings.as_view(), name="setting"),
	path('log_in', views.Login.as_view(), name="login"),
	path('new_ask', views.NewAsk.as_view(), name="ask"),
]