from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from apps.E_business_project_admin.serializers.group import GroupSerialzier
from apps.E_business_project_admin.serializers.permission import PermissionSerialzier
from apps.E_business_project_admin.utils import PageNum


class GroupView(ModelViewSet):
    '''用户管理'''
    serializer_class = GroupSerialzier
    queryset = Group.objects.all()
    pagination_class = PageNum

class GroupSimpleAPIView(APIView):
    '''获取权限表数据'''
    def get(self, request):
        pers = Permission.objects.all()
        ser = PermissionSerialzier(pers, many=True)
        return Response(ser.data)
