from __future__ import unicode_literals

from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models

from questions.manager import UserManager, TagManager, QuestionManager, AnswerManager, LikeManager

# Create your models here.

class CustomUser(AbstractUser):
    upload = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=False)    
    registration_date = models.DateTimeField(default=timezone.now, verbose_name="Дата решистрации", null=True)
    rating = models.IntegerField(default=0, verbose_name="Рейтинг пользователя", null=True)

    objects = UserManager()

    def __str__(self):
        return self.username

class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок ярлыка", null=True)

    objects = TagManager()

    def __str__(self):
        return self.title  

class Question(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, default='', verbose_name=u"Заголовок вопроса", null=True)
    text = models.TextField(verbose_name=u"Полное описание вопроса", null=True)
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса", null=True)
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0, null=False, verbose_name="Рейтинг вопроса")
    #votes = GenericRelation(Like, related_query_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']

class Answer(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)   
    text = models.TextField(verbose_name=u"Полное описание вопроса", null=False, default='')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время ответа", null=False)
    rating = models.IntegerField(default=0, null=False, verbose_name="Рейтинг ответа")
    approved = models.BooleanField(default=False, verbose_name=u"Одобрен автором вопроса")
    #votes = GenericRelation(Like, related_query_name='answers')

    objects = AnswerManager()

    def __str__(self):
        return self.text

class Like(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    objects = LikeManager()
    
    def __str__(self):
        return self.author + " liked"


def upload_img(self):
    if self.upload:
        from django.utils.safestring import mark_safe
        return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.upload.url))
    else:
        return '(Нет изображения)'
    upload_img.short_description = 'Картинка'
    upload_img.allow_tags = True
'''
def upload_img(self):
        if self.upload:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.upload.url))
        else:
            return '(Нет изображения)'
    upload_img.short_description = 'Картинка'
    upload_img.allow_tags = True
'''
