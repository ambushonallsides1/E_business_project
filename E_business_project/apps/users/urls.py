from django.conf.urls import url

from .import views

urlpatterns = [
    # 用户注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 用户名重复注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    # 手机号重复注册
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 用户中心
    url(r'^info/$', views.UserInfoView.as_view(), name='info'),
    # 用户登录
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # 退出登录
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 用户添加邮箱路由
    url(r'^emails/$', views.EmailView.as_view()),
    # 用户邮箱认证路由
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    # 展示收货地址界面
    url(r'^address/$', views.AddressView.as_view(), name='address'),
    # 新增地址路由
    url(r'^addresses/create/$', views.CreateAddressView.as_view()),
    # 修改地址路由
    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    # 设置默认地址
    url(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    # 修改地址标题
    url(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    # 修改密码
    url(r'^password/$', views.ChangePasswordView.as_view()),




]
