from django.db import models

# Create your models here.

class AnalysisResult(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, default='Male')
    age = models.IntegerField(default=0)
    division = models.CharField(max_length=100, default='Dhaka')
    area = models.CharField(max_length=255, default='-')
    house_type = models.IntegerField(default=0)
    ns1 = models.BooleanField(default=False)
    igm = models.BooleanField(default=False)
    igg = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis Result - {self.name or 'Unknown'}: NS1: {self.ns1}, IgM: {self.igm}, IgG: {self.igg}"


class SignsWarning(models.Model):
    """Separate model for Signs and Warnings page data"""
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, default='Male')
    age = models.IntegerField(default=0)
    division = models.CharField(max_length=100, default='Dhaka')
    area = models.CharField(max_length=255, default='-')
    house_type = models.IntegerField(default=0)
    ns1 = models.BooleanField(default=False)
    igm = models.BooleanField(default=False)
    igg = models.BooleanField(default=False)
    warning_prediction = models.BooleanField(default=False)
    warning_confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signs Warning - {self.name or 'Unknown'}: Warning: {self.warning_prediction}, Confidence: {self.warning_confidence}"