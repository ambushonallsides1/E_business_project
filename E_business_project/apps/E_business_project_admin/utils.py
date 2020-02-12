def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }

from django.contrib.auth.backends import ModelBackend
import re
from apps.users.models import User

class MeiduoModelBackend(ModelBackend):
    '''用户登录认证'''
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 判断是否通过vue组件发送请求\
        if request is None:
            try:
                user = User.objects.get(username=username, is_staff=True)
            except:
                return None
            # 判断密码
            if user.check_password(password):
                return user

        else:
            # 变量username的值，可以是用户名，也可以是手机号，需要判断，再查询
            try:
                user = User.objects.get(username=username)
            except:
                # 如果未查到数据，则返回None，用于后续判断
                try:
                    user = User.objects.get(mobile=username)
                except:
                    return None
                    # return None

            # 判断密码
            if user.check_password(password):
                return user
            else:
                return None


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class PageNum(PageNumberPagination):
    '''定义分页器'''
    page_size = 20  # 后端指定每页显示数量
    page_size_query_param = 'pagesize'
    max_page_size = 10

    # 重写分页返回方法，按照指定的字段进行分页数据返回
    def get_paginated_response(self, data):

        return Response({
            'count': self.page.paginator.count, # 总数量
            'lists': data,  # 用户数据
            'page' : self.page.number, # 当前页数
            'pages' : self.page.paginator.num_pages, # 总页数
            'pagesize':self.page_size  # 后端指定的页容量

        })