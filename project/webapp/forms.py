from django import forms

from account.models import Profile

class ProfileForm(forms.Form):
    # user_id = forms.ModelChoiceField(
    #     queryset=Profile.objects.all()
    # )
    position = forms.CharField(max_length=128)
    location = forms.CharField(max_length=1024)
    skills = forms.CharField(max_length=500)

    def __str__(self):
        return self.id