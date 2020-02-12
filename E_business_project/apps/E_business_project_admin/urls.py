from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from apps.E_business_project_admin.views import statistical
from apps.E_business_project_admin.views import user
from apps.E_business_project_admin.views import skus

urlpatterns = [
    # 用户认证
    url(r'^authorizations/$', obtain_jwt_token),
    # 用户总量统计
    url(r'^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    # 日增用户统计
    url(r'^statistical/day_increment/$', statistical.UserDailyCountView.as_view()),
    # 日活跃用户统计
    url(r'^statistical/day_active/$', statistical.UserDailyActiveCountView.as_view()),
    # 日下单用户量统计
    url(r'^statistical/day_orders/$', statistical.UserDailyOrderCountView.as_view()),
    # 月增用户统计
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    # 日分类商品访问量
    url(r'^statistical/goods_day_views/$', statistical.UserCategoryCountAPIView.as_view()),
    # 用户管理
    url(r'^users/$', user.UserListView.as_view()),
    # 商品分类三级
    url(r'^skus/categories/$', skus.SKUCategoriesView.as_view()),
    # 获取SPU表名称数据
    url(r'^goods/simple/$', skus.SPUSimpleView.as_view()),
    #
    url(r'^goods/(?P<pk>\d+)/specs/$', skus.SPUSpecView.as_view()),

]

# SKU表数据管理
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'skus', skus.SKUModelViewSet, basename='skus')
urlpatterns += router.urls
