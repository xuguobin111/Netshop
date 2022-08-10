from django.urls import path,re_path
from . import views
urlpatterns=[
    re_path(r'^$', views.order_view),
    re_path(r'^toOrder/$',views.toOrder),
    re_path(r'^toPay/$',views.toPay),
re_path(r'^checkPay/$',views.checkPay),
]