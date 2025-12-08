from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze_data, name='analyze_data'),
    path('signs-warnings/', views.signs_warnings, name='signs_warnings'),
    path('disease-analyst/', views.disease_analyst, name='disease_analyst'),
] 