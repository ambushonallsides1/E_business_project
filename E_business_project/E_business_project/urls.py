# 总路由文件
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 用户路由
    url(r'^', include('apps.users.urls', namespace='users')),
    # 首页
    url(r'^', include('apps.contents.urls', namespace='contents')),
    # 验证码
    url(r'^', include('apps.verifications.urls')),

]
