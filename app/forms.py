from django import forms
from .models import CustomUser,Info, Education

class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','email', 'password']
   

class UserDetailsForm(forms.ModelForm):
    username = forms.CharField(max_length=30, disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','title', 'address', 'email', 'phone', 'linkedin', 'twitter', 'instagram', 'about', 'latitude', 'longitude']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['name','yearfrom', 'yearto', 'about']
        
class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['head', 'body', 'certificate', 'linkedin']
        widgets = {
            'head': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the headline'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the description', 
                'rows': 4
            }),
            'certificate': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the certificate URL'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the LinkedIn URL'
            }),
        }
