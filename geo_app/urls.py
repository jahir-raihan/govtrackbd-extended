from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-details/', views.get_details, name='get-details'),
    path('update-ndre-projects-data/', views.update_ndre_projects_data, name='update-ndre-projects-data'),
    path('update-lged-projects-data/', views.update_lged_projects_data, name='update-lged-projects-data'),
    path('get-all-data/', views.get_data, name='get-all-data')


]