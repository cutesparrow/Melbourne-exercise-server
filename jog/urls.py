from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name = 'index'),
    path('path/',views.path,name = 'path'),
    path('sensorLocation/',views.sensorSituation,name = 'sensor situation'),
]
