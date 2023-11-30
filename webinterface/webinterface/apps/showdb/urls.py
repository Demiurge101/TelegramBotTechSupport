from django.urls import path 

from . import views

app_name = 'showdb'
urlpatterns = [
path('', views.index, name = 'index'),
path('orgs', views.orgs, name = 'orgs'),
path('stations', views.stations, name = 'stations'),
path('devices', views.devices, name = 'devices'),
path('auth', views.auth, name = 'auth'),
path('logout', views.log_out, name = 'logout'),

path('mkcb', views.mkcb, name = 'mkcb'),
path('add_mkcb_form', views.form_add_mkcb, name = 'add_mkcb_form'),
path('add_mkcb', views.add_mkcb, name = 'add_mkcb'),
path('mkcb/<decimal_number>', views.edit_mkcb_form, name = 'edit_mkcb_form'),
path('edit_mkcb', views.edit_mkcb, name = 'edit_mkcb'),
path('delete_mkcb/<decimal_number>', views.delete_mkcb, name = 'delete_mkcb')

# path('<int:botool_id>/', views.detail, name='detail'),
# path('<int:botool_id>/leave_comment', views.leave_comment, name='leave_comment')
]
