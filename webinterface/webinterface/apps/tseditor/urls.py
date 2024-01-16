from django.urls import path 

from . import views

app_name = 'tseditor'
urlpatterns = [
path('', views.index, name = 'index'),
path('title/<int:titleid>', views.title, name='title'),
path('title/<int:parentid>/add_title', views.add_title, name='add_title'),
path('title/<int:titleid>/update', views.update_title, name='update_title'),
path('title/<int:titleid>/delete', views.delete_title, name='delete_title'),


path('edit_document/<int:titleid>/<uuid>', views.document_edit_form, name='edit_document'),
path('upload_file/<int:titleid>', views.upload_file, name='upload_file'),
path('update_file/<int:titleid>/<uuid>', views.update_file, name='update_file'),
path('bond_file/<int:titleid>>', views.bond_file, name='bond_file'),
path('unbound_file/<int:titleid>/<uuid>', views.unbound_file, name='unbound_file'),
path('delete_file/<uuid>/<int:titleid>', views.delete_file, name='delete_file'),


# path('title/<int:parentid>/form_add_title', views.form_add_title, name='form_add_title')
# path('<int:botool_id>/', views.detail, name='detail'),
# path('<int:botool_id>/leave_comment', views.leave_comment, name='leave_comment')
]