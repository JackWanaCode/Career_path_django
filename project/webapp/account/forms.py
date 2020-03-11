from django import forms

class ProfileForm(forms.Form):
    position = forms.CharField(max_length=128)
    location = forms.CharField(max_length=1024)
    skills = forms.CharField(max_length=500)

    def __str__(self):
        return self.id