from django.contrib import admin
from .models import Blog, User, Resume, Education, Experience, JobNotifications, JobReceived
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','author','status','created_at','updated_at')
    list_filter = ('status','created_at','updated_at')
    search_fields = ('title','content','author')

admin.site.register(Blog,BlogAdmin)

admin.site.register(User) 

admin.site.register(Resume)

admin.site.register(Education)

admin.site.register(Experience)

admin.site.register(JobNotifications)

admin.site.register(JobReceived)