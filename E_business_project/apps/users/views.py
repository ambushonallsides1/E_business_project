import json

import re
from django import http
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.urls import reverse

from django.views import View
from pymysql import DatabaseError

from E_business_project.settings.dev import logger
from apps.users.models import User
from utils.response_code import RETCODE
from utils.views import LoginRequiredJSONMixin


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """实现退出登录逻辑"""
        # 清理session
        logout(request)
        # 退出登录，重定向到登录页
        response = redirect(reverse('contents:index'))
        # 退出登录时清除cookie中的username
        response.delete_cookie('username')

        return response

class LoginView(View):
    '''用户登录'''

    def get(self, request):
        """
          提供登录界面
          :param request: 请求对象
          :return: 登录界面
        """
        return render(request, 'login.html')

    def post(self, request):
        '''实现用户登录'''
        # 解析参数
        # 校验参数
        # 查询用户是否存在
        # 判断密码是否正确
        # 是否记住用户名密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 是否记住用户名参数
        remembered = request.POST.get('remembered')

        if not all([username, password]):
            return http.HttpResponseForbidden('参数不齐全')
        if not re.match(r'^[a-zA-Z0-9_-]{5-20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        if not re.match(r'^[a-zA-Z0-9]{8-20}$', password):
            return http.HttpResponseForbidden('请输入8-20个字符的密码')

        from django.contrib.auth import authenticate, login
        user = authenticate(username=username, password=password)

        login(request,user)

        if user is None:
            return render(request, 'login.html', context={'account_errmsg': '用户名或密码错误'})

        if remembered != 'on':
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)

        next = request.GET.get('next')
        if next:
            response = redirect(next)
        else:
            response = redirect(reverse('contents:index'))

        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        # 响应登录结果
        return response

class RegisterView(View):

    def get(self, request):
        '''用户注册界面'''
        return render(request, 'register.html')

    def post(self, request):
        '''实现用户注册'''

        # 接收参数
        # 参数校验
        # 保存数据
        # 用户名
        username = request.POST.get('username')
        #密码
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        #手机号
        mobile = request.POST.get('mobile')
        # 是否同意用户协议
        allow = request.POST.get('allow')
        # 短信验证码
        sms_code = request.POST.get('msg_code')

        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow, sms_code]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')

        from django_redis import get_redis_connection
        redis_code_client = get_redis_connection('sms_code')
        redis_code = redis_code_client.get("sms_%s" % mobile)

        if redis_code is None:
            return render(request, 'register.html', {'sms_code_errmsg': '无效的短信验证码'})

        if sms_code != redis_code.decode():
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})

        # 保存注册数据
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 实现状态保持
        login(request, user)

        response = redirect(reverse('contents:index'))

        # 注册时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        return response

class UsernameCountView(View):
    """判断用户名是否重复注册"""


    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})

class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})

class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active
        }
        return render(request, 'user_center_info.html', context=context)

class EmailView(LoginRequiredJSONMixin, View):

    def put(self, request):
        # 接收参数
        # 校验参数
        # 保存数据
        # 响应添加结果
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get('email')

        if not re.match(r'^[a-z0-9][\w/.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')
            # 赋值email字段
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})

        # 4.异步发送邮件
        from apps.users.utils import generate_verify_email_url
        verify_url = generate_verify_email_url(request.user)

        from celery_tasks.email.tasks import send_verify_email
        send_verify_email.delay(email, verify_url)

        # 响应添加邮箱结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})

class VerifyEmailView(LoginRequiredJSONMixin,View):

    def get(self, request):
        """实现邮箱验证逻辑"""
        # 接收参数
        token = request.GET.get('token')

        # 校验参数：判断token是否为空和过期，提取user
        if not token:
            return http.HttpResponseBadRequest('缺少token')
        from .utils import check_verify_email_token
        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseForbidden('无效的token')

        # 修改email_active的值为True
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮件失败')

        # 返回邮箱验证结果
        return redirect(reverse('users:info'))
