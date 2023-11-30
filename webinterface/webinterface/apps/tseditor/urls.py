from django.urls import path 

from . import views

app_name = 'tseditor'
urlpatterns = [
path('', views.index, name = 'index'),
# path('<int:botool_id>/', views.detail, name='detail'),
# path('<int:botool_id>/leave_comment', views.leave_comment, name='leave_comment')
]
