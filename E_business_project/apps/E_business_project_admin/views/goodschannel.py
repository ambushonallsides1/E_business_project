from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from apps.goods.models import GoodsChannel, GoodsChannelGroup
from apps.E_business_project_admin.serializers.goodschannel import GoodsChannelSerializer, GoodsChannelGroupSerializer
from apps.E_business_project_admin.utils import PageNum


class GoodsChannelModelViewSet(ModelViewSet):
    queryset = GoodsChannel.objects.all()
    serializer_class = GoodsChannelSerializer
    pagination_class = PageNum


class GoodsChannelGroupListAPIView(ListAPIView):
    queryset = GoodsChannelGroup.objects.all()
    serializer_class = GoodsChannelGroupSerializer