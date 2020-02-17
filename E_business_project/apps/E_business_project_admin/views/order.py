from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.E_business_project_admin.serializers.order import OrderSeriazlier
from apps.E_business_project_admin.utils import PageNum
from apps.orders.models import OrderInfo


class OrdersView(ModelViewSet):
    serializer_class = OrderSeriazlier
    queryset = OrderInfo.objects.all()
    pagination_class = PageNum

    # 在视图中定义status方法修改订单状态
    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        # 获取订单对象
        order = self.get_object()
        # 获取要修改的状态值
        status = request.data.get('status')
        # 修改订单状态
        order.status = status
        order.save()
        # 返回结果
        ser = self.get_serializer(order)
        return Response({
            'order_id': order.order_id,
            'status': status
        })