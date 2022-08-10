from django.urls import path,re_path
from userapp.models import *
from . import views
urlpatterns=[
   re_path(r'^register/$',views.RegisterView.as_view()),
   re_path(r'^center/$',views.CenterView.as_view()),
   re_path(r'^login/$',views.LoginView.as_view()),
re_path(r'^loadCode/$',views.loadCodeView.as_view()),
re_path(r'^checkCode/$',views.CheckCodeView.as_view()),
re_path(r'^logout/$',views.LogoutView.as_view()),
re_path(r'^address/$',views.AddressView.as_view()),
re_path(r'^loadAddr/$',views.loadAddrView),
]