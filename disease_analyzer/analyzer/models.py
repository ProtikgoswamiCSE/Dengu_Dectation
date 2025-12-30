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
    # Symptom fields (0 = No, 1 = Yes)
    symptom_mild_fever = models.IntegerField(default=0)
    symptom_eyelid_pain = models.IntegerField(default=0)
    symptom_headache = models.IntegerField(default=0)
    symptom_body_aches = models.IntegerField(default=0)
    symptom_nausea = models.IntegerField(default=0)
    symptom_skin_rash = models.IntegerField(default=0)
    symptom_fatigue = models.IntegerField(default=0)
    symptom_stomach_pain = models.IntegerField(default=0)
    symptom_dry_throat = models.IntegerField(default=0)
    symptom_lightheadedness = models.IntegerField(default=0)
    symptom_chest_pain = models.IntegerField(default=0)
    symptom_bleeding = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signs Warning - {self.name or 'Unknown'}: Warning: {self.warning_prediction}, Confidence: {self.warning_confidence}"