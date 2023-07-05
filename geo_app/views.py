from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from datetime import datetime
from .algorithms import *
from .data_collector import *
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProjectSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


def home(request):

    """Main Driver Function for User data visualization and filtering with necessary information."""

    if request.method == 'POST':
        query = request.POST
        projects = filter_projects(query)

        return JsonResponse({'projects': projects})

    date_ranges = get_date_ranges()
    agencies, projects = get_agency_and_project_names()
    context = {
        'start_dates': date_ranges[0],
        'end_dates': date_ranges[1],
        'agencies': agencies,
        'projects': projects

    }
    return render(request, 'home.html', context)


def get_details(request):

    """This Function will return the Project details along with location data in a viewable format."""

    project = Project.objects.get(pk=request.POST['project_id'])
    img = None
    lat, lng = None, None
    if project.category == 'NDRE':
        template = render_to_string('ndre-details.html', {'project': project}, request)
        p_type = 'NDRE'
        lat = project.latitude
        lng = project.longitude

    else:
        template = render_to_string('lged-details.html', {'project': project}, request)
        p_type = 'LGED'
        img = project.image

    return JsonResponse({'template': template, 'p_type': p_type, 'lat': lat, 'lng': lng, 'img': img,
                         'title': project.project_name})


def update_ndre_projects_data(request):

    """Updates NDRE data"""

    print('Updating database . . .')

    crawl_ndre()

    return HttpResponse('Updated Successfully !')


def update_lged_projects_data(request):

    """Updates LGED projects data"""

    print('Updating database . . .')

    crawl_lged()
    return HttpResponse('Updated Successfully !')


# API Endpoints

@csrf_exempt
@api_view(http_method_names=['GET', 'POST'])
def get_data(request):

    projects = Project.objects.all().order_by('-start_date')
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data,)
