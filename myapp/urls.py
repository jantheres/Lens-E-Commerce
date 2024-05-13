from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index,name='index'),
    path('admin_add',views.admin_lense_add,name='admin_add'),
    path('admin_update',views.admin_lense_update,name='admin_update'),
 
]
