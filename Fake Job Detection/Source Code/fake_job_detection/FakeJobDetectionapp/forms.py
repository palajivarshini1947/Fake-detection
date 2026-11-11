from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = '__all__'

class NotificationForm(forms.ModelForm):
    class Meta:
        model=Notification
        fields='__all__'

class CustomerRegiForm(forms.ModelForm):
    class Meta:
        model=CustomerRegi
        exclude = ['status']

class JobProviderForm(forms.ModelForm):
    class Meta:
        model=JobProvider
        exclude = ['status']

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        # We exclude provider and created_at because we handle those in views.py automatically
        exclude = ['provider', 'created_at']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']