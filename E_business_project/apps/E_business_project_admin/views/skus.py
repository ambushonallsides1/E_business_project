from rest_framework.viewsets import ModelViewSet
from apps.E_business_project_admin.serializers.skus import SKUSerializer, SKUCategorieSerializer, SPUSimpleSerializer, \
    SPUSpecSerialzier
from apps.E_business_project_admin.utils import PageNum
from apps.goods.models import SKU, GoodsCategory, SPU, SPUSpecification
from rest_framework.generics import ListAPIView


class SKUModelViewSet(ModelViewSet):
    serializer_class = SKUSerializer

    pagination_class = PageNum

    def get_queryset(self):
        '''获取SKU表数据'''
        # 提取keyword
        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(name=keyword)


class SKUCategoriesView(ListAPIView):
    '''获取三级分类信息'''
    serializer_class = SKUCategorieSerializer
    # 根据数据存储规律parent_id大于37为三级分类信息，查询条件为parent_id__gt=37
    queryset = GoodsCategory.objects.filter(parent_id__gt=37)


class SPUSimpleView(ListAPIView):
    '''获取SPU表名称数据'''

    serializer_class = SPUSimpleSerializer
    queryset = SPU.objects.all()


class SPUSpecView(ListAPIView):
    """获取SPU商品规格信息"""
    serializer_class = SPUSpecSerialzier

    # 因为我们继承的是ListAPIView，在拓展类中是通过get_queryset获取数据，但是我们现在要获取的是规格信息，所以重写get_queryset
    def get_queryset(self):
        pk = self.kwargs['pk']
        return SPUSpecification.objects.filter(spu_id=pk)
