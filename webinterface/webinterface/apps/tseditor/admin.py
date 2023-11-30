from django.contrib import admin

# Register your models here.

from .models import Contents, Titles

admin.site.register(Contents)
admin.site.register(Titles)