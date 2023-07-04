from django.contrib import admin
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_code', 'project_name', 'implementing_agency', ]
    search_fields = ['approval_ref', 'budget', 'capacity', 'category', 'completion_date', 'cumulative_expenditure',
                     'date_of_approval', 'district', 'division', 'executing_agency', 'expected_life_time',
                     'expected_till_now', 'note', 'project_name',
                     'funded_by', 'id', 'image', 'implementing_agency', 'latitude', 'location', 'longitude', 'ministry',
                     'pd_name', 'physical_progress', 'present_status', 'progress_reporting_date', 'project_code',
                     'sector', 'short_title', 'start_date', 'status', 'technology_type', 'upazilla']


admin.site.register(Project, ProjectAdmin)
