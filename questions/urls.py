from django.contrib import admin
from django.urls import path
from questions import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	# path('', views.TagPage.as_view(), name="tag"),


	# In working
	path('', views.index, name="index"),
	path('top', views.top, name="top"),
	path('new', views.new, name="new"),
	path('user/<int:id>/', views.profile, name="user"),
	path('user/questions/<int:id>/', views.user_questions, name='user_questions'),
	path('user/edit/', views.edit, name='edit'),
	path('question/<int:id>/', views.question_page, name='question_page'),
	path('question/<int:id>/add_answer/', views.new_answer, name='new_answer'),
	path('ask/', views.ask, name='ask'),
	path('log_in/', views.signin, name="login"),
	path('signout/', views.signout, name='signout'), 
	path('tag/<int:id>', views.tag, name='tag'),
	path('hot/<int:id>/', views.hot, name="hot"),
	path('registration/', views.registration, name='registration'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




