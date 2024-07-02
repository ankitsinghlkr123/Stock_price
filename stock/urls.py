from django.urls import path,include
from . import views

urlpatterns = [
    path('predict/', include('predict.urls')),
    path('', views.home,name='stock-home'),
    path('background/',include('background.urls')),
]