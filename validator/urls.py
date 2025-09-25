"""URLs for the validator app.

This module provides a minimal urlpatterns so the project can include
'validator.urls' without raising ModuleNotFoundError.
"""
from django.urls import path
from . import views

app_name = 'validator'

urlpatterns = [
    # root of the app -> upload view
    path('', views.upload_view, name='upload'),
]
