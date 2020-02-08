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
    # qq登录
    url(r'^', include('apps.oauth.urls', namespace="qq")),
    # 地址
    url(r'^', include('apps.areas.urls', namespace="areas")),
    # 首页商品
    url(r'^', include('apps.goods.urls', namespace='goods')),
    # 购物车
    url(r'^', include('apps.carts.urls', namespace='carts')),
    # 订单
    url(r'^', include('apps.orders.urls', namespace='orders')),
    # haystact搜索路由
    url(r'^search/', include('haystack.urls')),


]
