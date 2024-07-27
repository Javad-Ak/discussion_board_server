from django.contrib import admin

from discussions.models import Topic, Comment

admin.site.register(Topic)
admin.site.register(Comment)
