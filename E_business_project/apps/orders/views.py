import json
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.goods.models import SKU
from apps.users.models import Address
from django_redis import get_redis_connection


class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    def get(self, request):
        """提供订单结算页面"""
        # 获取用户
        # 查询订单数据
            # 查询地址
            # 查询商品
            # 查询价格
        # 构建返回数据

        user = request.user

        try:
            addresses = Address.objects.filter(user=user, is_deleted=False)
        except:
            addresses = None

        redis_client = get_redis_connection('carts')
        carts_data = redis_client.hgetall(user.id)
        carts_dict = {}
        for key, value in carts_data.items():
            sku_id = int(key.decode())
            sku_dict = json.loads(value.decode())
            if sku_dict['selected']:
                carts_dict[sku_id] = sku_dict

        # 3.计算金额 +邮费
        total_count = 0
        total_amount = Decimal(0.00)

        skus = SKU.objects.filter(id__in=carts_dict.keys())

        for sku in skus:
            sku.count = carts_dict[sku.id].get('count')
            sku.amount = sku.count * sku.price
            # 计算总数量和总金额
            total_count += sku.count
            total_amount += sku.count * sku.price

        # 运费
        freight = Decimal('10.00')

        # 4.构建前端显示的数据
        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount + freight,
            'default_address_id': user.default_address_id
        }

        return render(request, 'place_order.html', context)
