from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views import View
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login,logout

from account_module.forms import Register_Form,Login_Form


class RegisterView(View):
    def get(self, request):
        register_form = Register_Form()
        context = {
            "register_form": register_form
        }
        if(request.user.is_authenticated):
            return redirect(reverse("home-page"))
        return render(request, "account_module/register_page.html", context)

    def post(self, request):
        register_form = Register_Form(request.POST)
        print(f"POST is {request.POST}")
        if(register_form.is_valid()):
            user_email = register_form.cleaned_data.get("email")
            user : bool = User.objects.filter(email__iexact=user_email).exists()
            if(user):
                register_form.add_error("email", "ایمیل وارد شده متعلق به حساب کاربری دیگری میباشد")
            else:
                user_pass = register_form.cleaned_data.get("password")
                new_user = User(
                    email=user_email,
                    is_active=False,
                    email_activation_code=get_random_string(72),
                )
                new_user.set_password(user_pass)
                new_user.save()
                request.session["register_msg"] = True
                #todo : send user activition code
                return redirect(reverse("login_page"))
        context = {
            "register_form": register_form
        }
        return render(request, "account_module/register_page.html", context)

class LoginVeiw(View):
    def get(self, request):
        login_form = Login_Form()
        register_msg = request.session.get("register_msg", False)
        logout_msg = request.session.get("logout_msg", False)
        if(register_msg): del(request.session["register_msg"])
        if(logout_msg): del(request.session["logout_msg"])
        context = {
            "login_form": login_form,
            "register_msg": register_msg,
            "logout_msg": logout_msg
        }
        if(request.user.is_authenticated):
            return redirect(reverse("home-page"))
        return render(request, "account_module/login_page.html", context)

    def post(self, request):
        login_form = Login_Form(request.POST)
        if(login_form.is_valid()):
            user_email = login_form.cleaned_data.get("email")
            user_password = login_form.cleaned_data.get("password")
            user : User = User.objects.filter(email__iexact=user_email).first()
            if(user is not None):
                if(user.is_active):
                    check_pass = user.check_password(user_password)
                    if (check_pass):
                        login(request, user)
                        return redirect(reverse("home-page"))
                    else:
                        login_form.add_error("password", "ایمیل یا رمز عبور نادرست میباشد")
                else:
                    login_form.add_error("password", "حساب کاربری شما فعال نمیباشد")
            else:
                login_form.add_error("password", "ایمیل یا رمز عبور نادرست میباشد")
        context = {
            "login_form": login_form
        }
        return render(request, "account_module/login_page.html", context)

class logoutView(View):
    def get(self, request):
        logout(request)
        request.session["logout_msg"] = True
        request.session.set_expiry(1)
        return redirect(reverse("login_page"))