from django.urls import path
from .views import userPanelView

urlpatterns = [
    path("userpanel/", userPanelView.as_view(), name="userPanel")
]