from rest_framework.generics import ListCreateAPIView
from apps.E_business_project_admin.serializers.user import UserSerializer, UserAddSerializer
from apps.E_business_project_admin.utils import PageNum
from apps.users.models import User

class UserListView(ListCreateAPIView):

    pagination_class = PageNum

    def get_queryset(self):
        # 获取前端传递的keyword值
        keyword = self.request.query_params.get('keyword')
        # 如果keyword是空字符，则说明要获取所有用户数据
        if keyword is '' or keyword is None:
            return User.objects.all()
        else:
            return User.objects.filter(username=keyword)


    # 根据不同的请求方式返回不同序列化器
    def get_serializer_class(self):
        # 请求方式是GET，则是获取用户数据返回UserSerializer
        if self.request.method == 'GET':
            return UserSerializer
        else:
            # POST请求，完成保存用户，返回UserAddSerializer
            return UserAddSerializer