from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # url('login/', views.login, name='login'),
    path('marks/<int:form_id>/', views.marks, name='marks'),
]