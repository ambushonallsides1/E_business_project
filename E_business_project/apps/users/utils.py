from django.contrib.auth.backends import ModelBackend
import re
from .models import User

def get_user_by_account(account):
    """
     根据account查询用户
     :param account: 用户名或者手机号
     :return: user
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 手机号登录
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except:
        return None
    else:
        return user

class UsernameMobileAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
