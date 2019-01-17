from django.contrib import admin

# from .models import Post
''' Question, Answer, Tag, ''' 
from .models import CustomUser, Question, Answer, Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(CustomUser)
list_display = ['upload', 'upload_img',]
readonly_fields = ['image_img',]
fields = ['upload', 'upload_img',]
# admin.site.register(Post)

