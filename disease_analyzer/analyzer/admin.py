from django.contrib import admin
from .models import AnalysisResult, SignsWarning

# Register your models here.

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender', 'age', 'ns1', 'igm', 'igg', 'created_at')
    list_filter = ('gender', 'ns1', 'igm', 'igg', 'created_at')
    search_fields = ('name', 'area', 'division')

@admin.register(SignsWarning)
class SignsWarningAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender', 'age', 'ns1', 'igm', 'igg', 'warning_prediction', 'warning_confidence', 'created_at')
    list_filter = ('gender', 'ns1', 'igm', 'igg', 'warning_prediction', 'created_at')
    search_fields = ('name', 'area', 'division')
