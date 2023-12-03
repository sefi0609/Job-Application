from django import forms


class ApplicationFrom(forms.Form):
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    start_date = forms.DateField()
    resume = forms.FileField()
    occupation = forms.CharField(max_length=80)
