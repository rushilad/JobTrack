from django import forms
from .models import Job

class JobForm(forms.ModelForm):


    class Meta:
        model = Job
        fields = [
             "company",
            "role",
            "location",
            "salary",
            "status",
            "applied_date",
        ]