from rest_framework.viewsets import ModelViewSet
from apps.E_business_project_admin.utils import PageNum
from apps.E_business_project_admin.serializers.spec import SPUSpecificationSerializer
from apps.goods.models import SPUSpecification


class SpecsView(ModelViewSet):

    queryset = SPUSpecification.objects.all()
    serializer_class = SPUSpecificationSerializer

    pagination_class = PageNum


