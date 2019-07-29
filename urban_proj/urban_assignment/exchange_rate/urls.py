from django.urls import include, path
from . import views

urlpatterns = [
    path('chart', views.current_datetime, name='chart-view'),
    ]