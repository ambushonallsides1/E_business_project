import json

from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection

from apps.goods import models
from utils.response_code import RETCODE


class CartsView(LoginRequiredMixin, View):
    '''购物车'''

    def get(self, request):
        '''展示购物车'''
        # 查询数据库
        carts_redis_client = get_redis_connection('carts')

        # 获取当前用户的所有购物车数据
        carts_data = carts_redis_client.hgetall(request.user.id)

        carts_dict = {int(key.decode()): json.loads(value.decode()) for key, value in carts_data.items()}

        sku_ids = carts_dict.keys()

        skus = models.SKU.objects.filter(id__in=sku_ids)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': carts_dict.get(sku.id).get('count'),
                'selected': str(carts_dict.get(sku.id).get('selected')),  # 将True，转'True'，方便json解析
                'default_image_url': sku.default_image.url,
                'price': str(sku.price),  # 从Decimal('10.2')中取出'10.2'，方便json解析
                'amount': str(sku.price * carts_dict.get(sku.id).get('count')),
            })

        context = {
            'cart_skus': cart_skus,
        }

        # 渲染购物车页面
        return render(request, 'cart.html', context)

    def post(self, request):
        '''添加购物车'''
        '''
        sku_id 商品SKU编号
        count 商品数量
        selected 是否勾选
        '''

        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断sku_id是否存在
        try:
            models.SKU.objects.get(id=sku_id)
        except:
            return http.HttpResponseForbidden('商品不存在')
        # 判断count是否为数字
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden('参数count有误')
        # 判断selected是否为bool值
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')

        # 使用redis存储
        carts_redis_client = get_redis_connection('carts')

        # 获取以前数据库的数据
        user = request.user
        client_data = carts_redis_client.hgetall(user.id)

        # 如果商品已经存在就更新数据
        if str(sku_id).encode() in client_data:
            # 根据sku_id 取出商品
            child_dict = json.loads(client_data[str(sku_id).encode()].decode())
            #  个数累加
            child_dict['count'] += count
            # 更新数据
            carts_redis_client.hset(user.id, sku_id, json.dumps(child_dict))

        else:
            # 如果商品已经不存在--直接增加商品数据
            carts_redis_client.hset(user.id, sku_id, json.dumps({'count': count, 'selected': selected}))

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加购物车成功'})

    def put(self, request):
        """修改购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断sku_id是否存在
        try:
            sku = models.SKU.objects.get(id=sku_id)
        except:
            return http.HttpResponseForbidden('商品sku_id不存在')
        # 判断count是否为数字
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden('参数count有误')
        # 判断selected是否为bool值
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')

        # 1.链接 redis
        carts_redis_client = get_redis_connection('carts')
        # 2.覆盖redis以前的数据
        new_data = {'count': count, 'selected': selected}
        carts_redis_client.hset(request.user.id, sku_id, json.dumps(new_data))

        # 构建前端的数据
        cart_sku = {
            'id': sku_id,
            'count': count,
            'selected': selected,
            'name': sku.name,
            'default_image_url': sku.default_image.url,
            'price': sku.price,
            'amount': sku.price * count,
        }

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改购物车成功', 'cart_sku': cart_sku})

    def delete(self, request):
        """删除购物车"""
        # 接收和校验参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        pass

