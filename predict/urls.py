from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home,name='predict-home'),
    path('eval/',views.eval,name='eval')
]