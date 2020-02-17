from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.E_business_project_admin.serializers.group import GroupSerialzier
from apps.E_business_project_admin.serializers.permission import PermissionSerialzier, ContentTypeSerialzier, \
    AdminSerializer
from apps.E_business_project_admin.utils import PageNum
from apps.users.models import User


class PermissionView(ModelViewSet):
    serializer_class = PermissionSerialzier
    queryset = Permission.objects.all()
    pagination_class = PageNum

class ContentTypeAPIView(APIView):

    def get(self,request):
        # 查询全选分类
        content = ContentType.objects.all()
        # 返回结果
        ser = ContentTypeSerialzier(content, many=True)
        return Response(ser.data)

class AdminView(ModelViewSet):
    serializer_class = AdminSerializer
    # 获取管理员用户
    queryset = User.objects.filter(is_staff=True)
    pagination_class = PageNum

class AdminSimpleAPIView(APIView):

    def get(self,request):
        pers = Group.objects.all()
        ser = GroupSerialzier(pers, many=True)
        return Response(ser.data)