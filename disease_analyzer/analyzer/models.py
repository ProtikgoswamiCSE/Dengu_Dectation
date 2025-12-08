from django.db import models

# Create your models here.

class AnalysisResult(models.Model):
    ns1 = models.BooleanField(default=False)
    igm = models.BooleanField(default=False)
    igg = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis Result - NS1: {self.ns1}, IgM: {self.igm}, IgG: {self.igg}"
