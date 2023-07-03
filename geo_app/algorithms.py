import datetime
from .models import *
from django.db.models import Q

def get_date_ranges():

    """Get current date ranges for filtering purpose in frontEnd"""

    current_year = datetime.datetime.now().year
    start_dates = [i for i in range(2000, current_year)]
    end_dates = [i for i in range(2001, current_year + 20)]
    end_dates.sort(reverse=True)
    return [start_dates, end_dates]


def get_agency_and_project_names():

    """Get unique agency names and project names for filtering purpose in frontEnd"""

    agency_names = set()
    project_list = []

    for project in Project.objects.all():
        agency_names.add(project.implementing_agency)
        proj = {
            'project_name': f'{project.project_name} ({project.project_code})',
            'project_id': project.id
        }
        project_list.append(proj)

    return agency_names, project_list


def filter_projects(query):

    """Filters projects according to filtering criteria"""

    start_date = 1900 if not query['start_date'] else query['start_date']
    end_date = 9999 if not query['end_date'] else query['end_date']

    agency = query['agency']
    keyword = query['keyword']

    # Filtering by start, end dates and implementing agency
    projects = Project.objects.filter(implementing_agency__exact=agency)
    projects = projects.filter(
        Q(start_date__year__gte=int(start_date)) & Q(completion_date__year__lte=int(end_date))
    )

    # Filtering by search keyword
    projects = projects.filter(
        Q(project_name__icontains=keyword) | Q(project_code__icontains=keyword) |
        Q(implementing_agency__icontains=keyword) | Q(pd_name__icontains=keyword) | Q(sector__icontains=keyword) |
        Q(approval_ref__icontains=keyword) | Q(funded_by__icontains=keyword)| Q(executing_agency__icontains=keyword)
        | Q(ministry__icontains=keyword) | Q(category__icontains=keyword)
    )

    # Only taking project Name and project IDs for better performance

    project_list = []

    for project in projects:

        proj = {
            'project_name': f'{project.project_name} ({project.project_code})',
            'project_id': project.id
        }
        project_list.append(proj)

    return project_list


