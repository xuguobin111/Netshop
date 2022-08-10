from django.urls import path,re_path
from . import views
urlpatterns=[
    re_path(r'^$', views.CartView.as_view()),
    re_path(r'^queryAll',views.queryAll),
]