from django.conf.urls import url

from .import views

urlpatterns = [
    # 用户注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 用户名重复注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view(), name='register'),
    # 手机号重复注册
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.UsernameCountView.as_view()),
    # 用户中心
    url(r'^info/$', views.UserInfoView.as_view()),
]
