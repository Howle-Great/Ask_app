from django.contrib import admin

# from .models import Post
''' Question, Answer, Tag, ''' 
from .models import CustomUser, Question, Answer, Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(CustomUser)
# admin.site.register(Post)

