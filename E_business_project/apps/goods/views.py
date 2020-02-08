import json

from django import http
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.contents.utils import get_categories
from apps.goods import models, constants
from apps.goods.utils import get_breadcrumb
from utils.response_code import RETCODE
from django.contrib.auth.mixins import LoginRequiredMixin

class ListView(View):
    """商品列表页"""

    def get(self, request, category_id, page_num):
        """提供商品列表页"""

        # 判断category_id是否正确
        try:
            category = models.GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return http.HttpResponseNotFound('历史是不存在的')
        # 接收sort参数：如果用户不传，就是默认的排序规则
        sort = request.GET.get('sort', 'default')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)

        # 按照排序规则查询该分类商品sku信息
        if sort == 'price':
            # 按照价格由低到高
            sort_field = 'price'
        elif sort == 'hot':
            # 按照销量由高到低
            sort_field = '-sales'
        else:
            # 'price'和'sales'以外的所有排序方式都归为'default'
            sort_field = 'create_time'
        skus = models.SKU.objects.filter(category=category, is_launched=True).order_by(sort_field)

        # 创建分页器：每页N条记录
        paginator = Paginator(skus, constants.GOODS_LIST_LIMIT)
        # 获取每页商品数据
        try:
            page_skus = paginator.page(page_num)
        except :
            # 如果page_num不正确，默认给用户404
            return http.HttpResponseNotFound('空页面')
        # 获取列表页总页数
        total_page = paginator.num_pages

        # 渲染页面
        context = {
            'categories': categories,  # 频道分类
            'breadcrumb': breadcrumb,  # 面包屑导航
            'sort': sort,  # 排序字段
            'category': category,  # 第三级分类
            'page_skus': page_skus,  # 分页后数据
            'total_page': total_page,  # 总页数
            'page_num': page_num,  # 当前页码
        }

        return render(request, 'list.html',context=context)

class HotGoodsView(View):
    '''热销排行数据'''

    def get(self, request, category_id):
        '''
        提供商品热销排行JSON数据
        根据销量倒序
        category_id 商品分类ID，第三级分类
        '''
        skus = models.SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[0:2]

        # 构造数据
        hot_skus = []
        for sku in skus:
            hot_skus.append({
                'id': sku.id,
                'default_image_url': sku.default_image.url,
                'name': sku.name,
                'price': sku.price
            })

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'hot_skus': hot_skus})

class DetailView(View):
    """商品详情页"""

    def get(self, request, sku_id):
        """提供商品详情页"""
        # 获取当前sku的信息
        try:
            sku = models.SKU.objects.get(id=sku_id)
        except:
            return render(request, '404.html')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(sku.category)

        # 构建当前商品的规格键
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)
        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 构建不同规格参数（选项）的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数
            s_specs = s.specs.order_by('spec_id')
            # 用于形成规格参数-sku字典的键
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            # 向规格参数-sku字典添加记录
            spec_sku_map[tuple(key)] = s.id
        # 获取当前商品的规格信息
        goods_specs = sku.spu.specs.order_by('id')
        # 若当前sku的规格信息不完整，则不再继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 复制当前sku的规格键
            key = sku_key[:]
            # 该规格的选项
            spec_options = spec.options.all()
            for option in spec_options:
                # 在规格参数sku字典中查找符合当前规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options

        # 渲染页面
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs,
        }
        return render(request, 'detail.html', context=context)

class DetailVisitView(View):
    """详情页分类商品访问量"""

    def post(self, request, category_id):
        try:
            # 1.获取当前商品
            category = models.GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return http.HttpResponseNotFound('缺少必传参数')

        # 2.查询日期数据
        from datetime import datetime
        # 将日期按照格式转换成字符串
        today_str = datetime.now().strftime('%Y-%m-%d')
        # 将字符串再转换成日期格式
        today_date = datetime.strptime(today_str, '%Y-%m-%d')

        from apps.goods.models import GoodsVisitCount
        try:
            # 3.如果有当天商品分类的数据  就累加数量
            count_data = category.goodsvisitcount_set.get(date=today_date)
        except:
            # 4. 没有, 就新建之后在增加
            count_data = GoodsVisitCount()

        try:
            count_data.count += 1
            count_data.category = category
            count_data.save()
        except Exception as e:
            return http.HttpResponseServerError('新增失败')

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

class UserBrowseHistory(LoginRequiredMixin, View):
    """用户浏览记录"""

    def get(self, request):
        """获取用户浏览记录"""
        # 获取Redis存储的sku_id列表信息
        redis_conn = get_redis_connection('history')
        sku_ids = redis_conn.lrange('history_%s' % request.user.id, 0, -1)

        # 根据sku_ids列表数据，查询出商品sku信息
        skus = []
        for sku_id in sku_ids:
            sku = models.SKU.objects.get(id=sku_id)
            skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'skus': skus})

    def post(self, request):
        """保存用户浏览记录"""
        # 1.接收json参数
        sku_id = json.loads(request.body.decode()).get('sku_id')

        # 2.根据sku_id 查询sku
        try:
            sku = models.SKU.objects.get(id=sku_id)
        except:
            return http.HttpResponseForbidden('商品不存在!')

        # 3.如果有sku,保存到redis
        history_redis_client = get_redis_connection('history')
        history_key = 'history_%s' % request.user.id

        redis_pipeline = history_redis_client.pipeline()
        # 3.1 去重
        history_redis_client.lrem(history_key, 0, sku_id)
        # 3.2 存储
        history_redis_client.lpush(history_key, sku_id)
        # 3.3 截取 5个
        history_redis_client.ltrim(history_key, 0, 4)
        redis_pipeline.execute()

        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
