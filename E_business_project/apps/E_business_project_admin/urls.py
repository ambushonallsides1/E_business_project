from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from apps.E_business_project_admin.views import statistical, spu, spec, option, image, order, permission, group, brand, \
    goodschannel
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

    # sku相关
    # 商品分类三级
    url(r'^skus/categories/$', skus.SKUCategoriesView.as_view()),
    # 获取SPU表名称数据
    url(r'^goods/simple/$', skus.SPUSimpleView.as_view()),
    # 获取SPU商品规格信息
    url(r'^goods/(?P<pk>\d+)/specs/$', skus.SPUSpecView.as_view()),

    # spu相关
    # 获取品牌信息
    url(r'^goods/brands/simple/$', spu.SPUBrandView.as_view()),
    # 获取一级分类信息
    url(r'^goods/channel/categories/$', spu.ChannelCategorysOneView.as_view()),
    # 获取二级和三级分类
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', spu.ChannelCategoryTwoThreeView.as_view()),
    # 规格选项表数据
    url(r'^goods/specs/simple/$', option.OptionSimple.as_view()),
    # 获取sku表id
    url(r'^skus/simple/$', image.SKUView.as_view()),
    # 保存权限表数据
    url(r'^permission/content_types/$', permission.ContentTypeAPIView.as_view()),
    # 权限表数据
    url(r'^permission/simple/$', group.GroupSimpleAPIView.as_view()),
    url(r'^permission/groups/simple/$', permission.AdminSimpleAPIView.as_view()),

    # 频道组显示goods/channel_types/
    url(r'^goods/channel_types/$', goodschannel.GoodsChannelGroupListAPIView.as_view()),
    # 一级分类goods/categories/
    url(r'^goods/categories/$', spu.ChannelCategorysOneView.as_view()),

]


from rest_framework.routers import DefaultRouter
router = DefaultRouter()

#######spu信息
router.register(r'goods/brands', brand.BrandModelViewSet, basename='brands')
urlpatterns += router.urls

#########商品频道管理goods/channels
router.register(r'goods/channels', goodschannel.GoodsChannelModelViewSet, basename='channel')
urlpatterns += router.urls

# 图片列表数据
router.register(r'skus/images', image.ImageView, basename='images')
urlpatterns += router.urls

# 用户权限表列表数据
router.register(r'permission/perms', permission.PermissionView, basename='perms')
urlpatterns += router.urls

# 管理员管理
router.register(r'permission/admins', permission.AdminView, basename='admins')
urlpatterns += router.urls

# 用户分组
router.register(r'permission/groups', group.GroupView, basename='groups')
urlpatterns += router.urls

# 订单表数据
router.register(r'orders', order.OrdersView, basename='orders')
urlpatterns += router.urls

# SKU表数据管理
router.register(r'skus', skus.SKUModelViewSet, basename='skus')
urlpatterns += router.urls

# spec规格表数据
router.register(r'goods/specs',spec.SpecsView,basename='spec')
urlpatterns += router.urls

# spu表管理
router.register(r'goods',spu.SPUGoodsView,basename='spu')
urlpatterns += router.urls

# 规格选项表数据
router.register(r'specs/options',option.OptionsView,basename='options')
urlpatterns += router.urls



