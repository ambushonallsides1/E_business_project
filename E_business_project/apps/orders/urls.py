from django.conf.urls import url

from . import views

urlpatterns = [
    # 订单
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view(), name='settlement'),
]
