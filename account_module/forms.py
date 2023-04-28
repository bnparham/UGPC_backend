from django import forms
from django.core.exceptions import ValidationError
from django.core import validators


class Register_Form(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(Register_Form, self).__init__(*args, **kwargs)

    name = forms.CharField(
        label="نام و نام خانوادگی",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "register_name",
            }
        ),
    )
    username = forms.CharField(
        label="نام کاربری",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "username",
            }
        ),
    )
    email = forms.CharField(
        label="ایمیل",
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class" : "form-control",
                "id" : "register_email"
            }
        ),
        validators=[
            validators.EmailValidator(message="ایمیل صحیح نمیباشد"),
        ]
    )
    uid = forms.CharField(
        label="شماره دانشجویی",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "register_uid",
            }
        ),
    )
    password = forms.CharField(
        label="رمز عبور",
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "register_pass"
            }
        )
    )
    repeat_password = forms.CharField(
        label="تکرار رمز عبور",
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "register_re_pass"
            }
        )
    )

    def clean_repeat_password(self):
        password = self.cleaned_data.get("password")
        repeat_password = self.cleaned_data.get("repeat_password")
        if(password == repeat_password):
            return repeat_password
        self.request.session["notMatch_pass_rePass"] = True
        raise ValidationError("رمز عبور مطابقت ندارد")

class Login_Form(forms.Form):
    email = forms.CharField(
        label="ایمیل",
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class" : "form-control",
                "id" : "login_email",
            }
        ),
    )
    password = forms.CharField(
        label="رمز عبور",
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "login_pass",
            }
        ),
    )

class EditUserInfoForm(forms.Form):
    name = forms.CharField(
        label="نام و نام خانوادگی",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "register_name",
            }
        ),
    )
    username = forms.CharField(
        label="نام کاربری",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "username",
            }
        ),
    )
    email = forms.CharField(
        label="ایمیل",
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class" : "form-control",
                "id" : "register_email"
            }
        ),
        validators=[
            validators.EmailValidator(message="ایمیل صحیح نمیباشد"),
        ]
    )
    uid = forms.CharField(
        label="شماره دانشجویی",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "register_uid",
            }
        ),
    )