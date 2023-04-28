from django.urls import path

from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register_page"),
    path("login/", LoginVeiw.as_view(), name="login_page"),
    path("logout/", logoutView.as_view(), name="logout_page"),
    path("changeUserType/", changeUserType.as_view(), name="change_userType"),
    path('activate/<uidb64>/<token>', RegisterView.activate, name='activate'),
    path('editUserInfo', editUserInfo.as_view(), name="editUserInfo"),
]