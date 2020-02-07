from django.conf.urls import url

from .import views

urlpatterns = [
    # qq登录
    url(r'^qq/login/$', views.QQAuthURLView.as_view(), name='qqlogin'),
    # qq登录回调处理
    url(r'^oauth_callback/$', views.QQAuthUserView.as_view()),

]
