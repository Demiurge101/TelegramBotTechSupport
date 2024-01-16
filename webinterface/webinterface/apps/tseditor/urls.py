from django.urls import path 

from . import views

app_name = 'tseditor'
urlpatterns = [
path('', views.index, name = 'index'),
path('title/<int:titleid>', views.title, name='title'),
path('title/<int:parentid>/add_title', views.add_title, name='add_title'),
path('title/<int:titleid>/update', views.update_title, name='update_title'),
path('title/<int:titleid>/delete', views.delete_title, name='delete_title'),
# path('title/<int:parentid>/form_add_title', views.form_add_title, name='form_add_title')
# path('<int:botool_id>/', views.detail, name='detail'),
# path('<int:botool_id>/leave_comment', views.leave_comment, name='leave_comment')
]