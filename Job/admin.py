from django.contrib import admin
from .models import JobApplication,SavedJob
# Register your models here.
admin.site.register(JobApplication)
admin.site.register(SavedJob)