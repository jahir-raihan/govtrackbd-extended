from django.db import models


class Project(models.Model):

    """This model will hold the project details"""

    project_name = models.CharField(max_length=500)
    implementing_agency = models.CharField(max_length=200)
    technology_type = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.CharField(max_length=20, null=True, blank=True)
    project_code = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(max_length=20, null=True, blank=True, default='1900-01-01')
    completion_date = models.DateField(max_length=20, null=True, blank=True)
    budget = models.CharField(max_length=20, null=True, blank=True, default='N/A')
    division = models.CharField(max_length=20, null=True, blank=True, default='N/A')
    district = models.CharField(max_length=20, null=True, blank=True, default='N/A')
    upazilla = models.CharField(max_length=20, null=True, blank=True, default='N/A')
    location = models.CharField(max_length=100, null=True, blank=True, default='N/A')
    latitude = models.CharField(max_length=30, null=True, blank=True, default='N/A')
    longitude = models.CharField(max_length=30, null=True, blank=True, default='N/A')

    present_status = models.CharField(max_length=60, null=True, blank=True, default='N/A')
    note = models.TextField(null=True, blank=True, default='N/A')
    expected_life_time = models.CharField(max_length=50, null=True, blank=True, default='N/A')
    expected_till_now = models.CharField(max_length=50, null=True, blank=True, default='N/A')

    pd_name = models.CharField(max_length=30, null=True, blank=True, default='N/A')
    date_of_approval = models.CharField(max_length=15, null=True, blank=True, default='N/A')
    cumulative_expenditure = models.CharField(max_length=50, null=True, blank=True, default='N/A')

    physical_progress = models.CharField(max_length=5, null=True, blank=True, default='N/A')
    short_title = models.CharField(max_length=20, null=True, blank=True, default='N/A')
    approval_ref = models.CharField(max_length=10, null=True, blank=True, default='N/A')
    sector = models.CharField(max_length=25, null=True, blank=True, default='N/A')
    status = models.CharField(max_length=100, null=True, blank=True, default='N/A')
    funded_by = models.CharField(max_length=30, null=True, blank=True, default='N/A')
    image = models.CharField(max_length=150, null=True, blank=True, default='N/A')

    progress_reporting_date = models.CharField(max_length=15, null=True, blank=True, default='N/A')
    ministry = models.CharField(max_length=50, null=True, blank=True, default='N/A')
    executing_agency = models.CharField(max_length=50, null=True, blank=True, default='N/A')

    category = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.project_name}"

