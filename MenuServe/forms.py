from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError

class SignInForm(forms.Form):
    username = fields.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={'class': "form-control",'placeholder':'username',}),
        error_messages={
            "required":"username can't be empty",
            "max_length":"username can't be more than 20"
        }
    )
    firstname = fields.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={'class': "form-control",'placeholder':'firstname',}),
        error_messages={
            "required":"firstname can't be empty",
            "max_length":"firstname can't be more than 20"
        }
    )
    lastname = fields.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={'class': "form-control",'placeholder':'lastname',}),
        error_messages={
            "required":"lastname can't be empty",
            "max_length":"lastname can't be more than 20"
        }
    )
    password1 = fields.CharField(
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': "form-control",'placeholder':'password',}),
        error_messages={
            "required":"password can't be empty",
            "min_length": "password can't be less than 6",
            "max_length": "password can't be more than 20"
        }
    )
    password2 = forms.fields.CharField(required=False,widget=forms.PasswordInput(attrs={'class': "form-control",'placeholder':'confirm password',}),)

    def clean_password2(self):
        if not self.errors.get("password1"):
            if self.cleaned_data["password2"] != self.cleaned_data["password1"]:
                raise ValidationError("The passwords you inputed are different ")
            return self.cleaned_data


class LogInForm(forms.Form):
    username = fields.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={'class': "form-control",'placeholder':'username','id':'username',}),
        error_messages={
            "required":"username can't be empty",
            "max_length":"username can't be more than 20"
        }
    )
    password = fields.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control",'placeholder':'password','id':'password',}),
        error_messages={
        	"required":"password can't be empty"
        }
    )

