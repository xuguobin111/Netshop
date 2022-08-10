from django.urls import path,re_path
from . import views
urlpatterns=[
    re_path(r'^$', views.IndexView.as_view()),
    re_path(r'^category/(?P<cid>\d+)$',views.IndexView.as_view()),
    re_path(r'^category/(?P<cid>\d+)/page/(?P<num>\d+)$',views.IndexView.as_view()),
    re_path(r'^goodsdetails/(\d+)$',views.DetailView.as_view())
]