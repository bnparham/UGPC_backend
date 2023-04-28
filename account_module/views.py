from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views import View
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login,logout
from django.db.models import Q

from account_module.forms import Register_Form,Login_Form
from team_module.models import teamsModel

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token

class RegisterView(View):
    def get(self, request):
        register_form = Register_Form(request=request)
        context = {
            "register_form": register_form
        }
        if(request.user.is_authenticated):
            return redirect(reverse("home-page"))
        return render(request, "account_module/register_page.html", context)

    def post(self, request):
        register_form = Register_Form(request.POST, request=request)
        if(register_form.is_valid()):
            user_email = register_form.cleaned_data.get("email")
            user_uid = register_form.cleaned_data.get("uid")
            user_username = register_form.cleaned_data.get("username")
            user_name = register_form.cleaned_data.get("name")
            user : bool = User.objects.filter(email__iexact=user_email).exists()
            if(User.objects.filter(username=user_username).exists()):
                request.session["duplicate_username"] = True
                return redirect(reverse("home-page"))
            if(User.objects.filter(uid=user_uid).exists()):
                request.session["duplicate_uid"] = True
                return redirect(reverse("home-page"))
            if(user):
                # register_form.add_error("email", "ایمیل وارد شده متعلق به حساب کاربری دیگری میباشد")
                request.session["duplicate_email"] = True
                return redirect(reverse("home-page"))
            else:
                user_pass = register_form.cleaned_data.get("password")
                new_user = User(
                    email=user_email,
                    is_active=False,
                    email_activation_code=0,
                    uid=user_uid,
                    first_name=user_name,
                    username=user_username,
                )
                new_user.set_password(user_pass)
                new_user.save()
                new_user.email_activation_code = account_activation_token.make_token(new_user)
                new_user.save()
                
                #email
                to_email=user_email
                mail_subject = 'حساب کاربری رو فعال کن!'
                message = render_to_string('account_module/email_activation.html', {
                    'user': user_username,
                    'full_name': f'{user_name}',
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': account_activation_token.make_token(new_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.content_subtype = 'html'
                
                if email.send():
                    request.session["register_msg"] = True
                else:
                    request.session["failed_register_msg"] = True
                    new_user.delete()
                                        
                return redirect(reverse("home-page"))
        return redirect(reverse("home-page"))
    
    def activate(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            request.session['email_activated']=True
            login(request,user)
            return redirect(reverse("home-page"))
        else:
            request.session['email_didnt_activated']=True
            
        return redirect(reverse("home-page"))
    

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
                        # login_form.add_error("password", "ایمیل یا رمز عبور نادرست میباشد")
                        request.session["email_pass_wrong_msg"] = True
                else:
                    # login_form.add_error("password", "حساب کاربری شما فعال نمیباشد")
                    request.session["active_acc_msg"] = True
            else:
                # login_form.add_error("password", "ایمیل یا رمز عبور نادرست میباشد")
                request.session["email_pass_wrong_msg"] = True
        return redirect(reverse("home-page"))

class logoutView(View):
    def get(self, request):
        logout(request)
        request.session["logout_msg"] = True
        request.session.set_expiry(1)
        return redirect(reverse("home-page"))

class changeUserType(View):
    def get(self, request):
        empty_teamName_msg = request.session.get("empty_teamName_msg", False)
        if(empty_teamName_msg): del(request.session["empty_teamName_msg"])

        user:User = User.objects.get(email__iexact=request.user.email)
        findUserTeam = teamsModel.objects.filter(capitan=user).exists()
        if(findUserTeam):
            userTeamName = teamsModel.objects.get(capitan=user).teamName
        else:
            userTeamName = False
        context = {
            "userTeamName" : userTeamName,
            "empty_teamName_msg" : empty_teamName_msg,
        }
        return render(request, "account_module/userType.html", context)

    def post(self, request):
        is_cap = int(request.POST.get("options-outlined"))
        user:User = User.objects.get(email__iexact=request.user.email)
        findUserTeam = teamsModel.objects.filter(capitan=user).exists()
        if is_cap == 1 and not user.is_capitan:
            user.is_capitan = True
            findGroupThatHasThisUser = teamsModel.objects.filter(Q(teamMate1=user) | Q(teamMate2=user)).exists()
            if(findGroupThatHasThisUser):
                try:
                    t = teamsModel.objects.get(teamMate1=user)
                    t.teamMate1 = None
                except:
                    t = teamsModel.objects.get(teamMate2=user)
                    t.teamMate2 = None
                t.save()
            user.save()
        elif is_cap == 0 and user.is_capitan:
            user.is_capitan = False
            user.has_team = False
            if findUserTeam:
                teamsModel.objects.filter(capitan=user).delete()
            user.save()
        elif is_cap == 1 and user.is_capitan:
            group_name = request.POST.get("teamName")
            if findUserTeam:
                teamName = teamsModel.objects.get(capitan=user)
                if teamName.teamName != group_name and group_name != "":
                    teamName.teamName = group_name
                    teamName.save()
            else:
                if(group_name == None or group_name == "" or len(group_name)==0):
                    request.session["empty_teamName_msg"] = True
                else:
                    newTeam = teamsModel(capitan=user, teamName=group_name, teamMate1=None, teamMate2=None)
                    user.has_team = True
                    newTeam.save()
                    user.save()
                return redirect(reverse("userPanel"))
