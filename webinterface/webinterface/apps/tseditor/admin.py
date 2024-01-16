from django.contrib import admin

# Register your models here.

from .models import Contents, Titles, Files, Filebond

admin.site.register(Contents)
admin.site.register(Titles)
admin.site.register(Files)
admin.site.register(Filebond)