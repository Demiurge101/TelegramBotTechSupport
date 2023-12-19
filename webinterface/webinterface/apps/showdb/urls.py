from django.urls import path

from . import views

app_name = 'showdb'
urlpatterns = [
path('', views.index, name = 'index'),
path('orgs', views.orgs, name = 'orgs'),
path('auth', views.auth, name = 'auth'),
path('logout', views.log_out, name = 'logout'),

path('mkcb', views.mkcb, name = 'mkcb'),
path('add_mkcb_form', views.form_add_mkcb, name = 'add_mkcb_form'),
path('add_mkcb', views.add_mkcb, name = 'add_mkcb'),
path('mkcb/<decimal_number>', views.edit_mkcb_form, name = 'edit_mkcb_form'),
path('edit_mkcb', views.edit_mkcb, name = 'edit_mkcb'),
path('delete_mkcb/<decimal_number>', views.delete_mkcb, name = 'delete_mkcb'),

path('documents', views.documents, name='documents'),
path('add_document', views.document_add_form, name='add_document'),
path('edit_document/<uuid>', views.document_edit_form, name='edit_document'),
path('delete_document/<uuid>', views.delete_file, name='delete_document'),
path('upload_file', views.upload_file, name='upload_file'),
path('upload_file/<number>', views.upload_file, name='upload_file'),
path('upload_file/<number>/<backlink>', views.upload_file, name='upload_file'),

path('stations', views.stations, name = 'stations'),
path('add_station_form', views.form_add_station, name = 'add_station_form'),
# path('add_station', views.add_station, name = 'add_station'),
path('station/<number>', views.edit_station_form, name = 'edit_station_form'),
path('edit_station', views.edit_station, name = 'edit_station'),
path('delete_station/<number>', views.delete_station, name = 'delete_station'),

path('devices', views.devices, name = 'devices'),
path('add_device_form', views.form_add_device, name = 'add_device_form'),
# path('add_device', views.add_device, name = 'add_device'),
path('device/<number>', views.edit_device_form, name = 'edit_device_form'),
path('edit_device', views.edit_device, name = 'edit_device'),
path('delete_device/<int:number>', views.delete_device, name = 'delete_device'),




# path('<int:botool_id>/', views.detail, name='detail'),
# path('<int:botool_id>/leave_comment', views.leave_comment, name='leave_comment')
]
