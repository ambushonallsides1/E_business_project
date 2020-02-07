from django.conf import settings
from django.contrib.auth.backends import ModelBackend
import re

from E_business_project.settings.dev import logger
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

def generate_verify_email_url(user):
    """
    :param user: 用户对象
    :return:
    """
    # 1.加密的数据
    data_dict = {'user_id': user.id,"email": user.email}

    # 2. 进行加密数据
    from utils.secret import SecretOauth
    secret_data = SecretOauth().dumps(data_dict)

    # 3. 返回拼接url
    active_url = settings.EMAIL_ACTIVE_URL + '?token=' + secret_data
    return active_url

def check_verify_email_token(token):
    from utils.secret import SecretOauth
    try:
        token_dict = SecretOauth().loads(token)
    except:
        return None

    try:
        user = User.objects.get(id=token_dict['user_id'], email=token_dict['email'])
    except Exception as e:
        logger.error(e)
        return None
    else:
        return user

