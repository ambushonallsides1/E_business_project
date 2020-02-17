from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.goods.models import Brand
from apps.E_business_project_admin.serializers.brand import BrandSerializer
from apps.E_business_project_admin.utils import PageNum


class BrandModelViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = PageNum

#{'Group name': 'group1',
# 'Status': 'Upload successed.',
# 'Remote file_id': 'group1/M00/00/02/wKh_gV2AltyAGDE1AAB_OgW2yjA371.jpg',
# 'Uploaded size': '31.00KB',
# 'Local file name': '/home/python/Desktop/js/i5.jpg',
#  'Storage IP': '192.168.127.129'}

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        first_letter = request.data.get('first_letter')
        # 获取图片
        logo = request.FILES.get('logo')
        # 导包 创建链接
        from fdfs_client.client import Fdfs_client
        client = Fdfs_client('utils/fastdfs/client.conf')

        ret = client.upload_by_buffer(logo.read())
        if ret['Status'] != 'Upload successed.':
            return Response(status=status.HTTP_403_FORBIDDEN)
        logo_url = ret['Remote file_id']
        brand = Brand.objects.create(name=name,first_letter=first_letter,logo=logo_url)
        return Response({
            'id':brand.id,
            'name':name,
            'first_letter':first_letter,
            'logo':logo_url
        },status=201)

    def update(self, request, *args, **kwargs):
        name = request.data.get('name')
        first_letter = request.data.get('first_letter')
        # 获取图片
        logo = request.FILES.get('logo')
        # 导包 创建链接
        from fdfs_client.client import Fdfs_client
        client = Fdfs_client('utils/fastdfs/client.conf')

        ret = client.upload_by_buffer(logo.read())
        if ret['Status'] != 'Upload successed.':
            return Response(status=status.HTTP_403_FORBIDDEN)
        logo_url = ret['Remote file_id']
        brand = Brand.objects.get(id=kwargs['pk'])
        brand.logo=logo_url
        brand.name=name
        brand.save()
        return Response({
            'id': brand.id,
            'name': name,
            'first_letter': first_letter,
            'logo': logo_url
        }, status=201)