from django import forms
from .models import Species, Observation
from django.forms.widgets import DateTimeInput


#Validating and creating/editing Species model entries
class SpeciesForm(forms.ModelForm):
    class Meta:
        model = Species
        fields=['name','description','feather_color']

    #Ensure name only contains letters and spaces
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.replace(' ', '').isalpha():
            raise forms.ValidationError('Name must only contain letters and spaces')
        return name
    
    #Ensure color only contains letters and spaces
    def clean_feather_color(self):
        color = self.cleaned_data['feather_color']
        if not color.replace(' ','').isalpha():
            raise forms.ValidationError('Feather color must only contain letters and spaces')
        return color
    
#Validating and creating/editing Observation model entries
class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['species','location','sex','time']
        widgets = {
            'time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    #Validation to ensure only letters and spaces
    def clean_sex(self):
        sex = self.cleaned_data['sex']
        valid_choices = ['Male','Female','Unknown']
        if sex not in valid_choices:
            raise forms.ValidationError(f"Sex must be one of {', '.join(valid_choices)}.")
        return sex