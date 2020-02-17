from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from apps.E_business_project_admin.serializers.option import OptionSerialzier, OptionSpecificationSerializer
from apps.E_business_project_admin.utils import PageNum
from apps.goods.models import SpecificationOption, SPUSpecification


class OptionsView(ModelViewSet):
    """
            规格选项表的增删改查
    """
    serializer_class = OptionSerialzier
    queryset = SpecificationOption.objects.all()
    pagination_class = PageNum

class OptionSimple(ListAPIView):
    """
        获取规格信息
    """
    serializer_class = OptionSpecificationSerializer
    queryset = SPUSpecification.objects.all()