from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze_data, name='analyze_data'),
    path('signs-warnings/', views.signs_warnings, name='signs_warnings'),
    path('disease-analyst/', views.disease_analyst, name='disease_analyst'),
    path('save-disease-data/', views.save_disease_data, name='save_disease_data'),
    path('delete-all-disease-data/', views.delete_all_disease_data, name='delete_all_disease_data'),
    path('save-signs-warnings-data/', views.save_signs_warnings_data, name='save_signs_warnings_data'),
    path('delete-all-signs-warnings-data/', views.delete_all_signs_warnings_data, name='delete_all_signs_warnings_data'),
] 