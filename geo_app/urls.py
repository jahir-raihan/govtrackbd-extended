from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-details/', views.get_details, name='get-details'),

]