from django.contrib import admin
from MainApp.models import Snippet,Comment
admin.site.register([Snippet,Comment])
