from django.conf.urls import url

from . import views

urlpatterns = [
    # 订单展示
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view(), name='settlement'),
    # 提交订单
    url(r'^orders/commit/$', views.OrderCommitView.as_view(), name='commit'),
    # 展示提交订单成功页面
    url(r'^orders/success/$', views.OrderSuccessView.as_view(), name='success'),
    # 我的订单展示
    url(r'^orders/info/(?P<page_num>\d+)/$', views.UserOrderInfoView.as_view(), name='orders_info'),
    # 订单评价
    url(r'^orders/comment/$', views.OrderCommentView.as_view(), name='orders_comment'),
    # 详情页展示评价信息
    url(r'^comments/(?P<sku_id>\d+)/$', views.GoodsCommentView.as_view()),
]
