from django.contrib import admin

# Register your models here.

from .models import Clients, DecimalNumbers, Devices, Files, Stations, Users

admin.site.register(Clients)
admin.site.register(DecimalNumbers)
admin.site.register(Stations)
admin.site.register(Files)
admin.site.register(Devices)
admin.site.register(Users)