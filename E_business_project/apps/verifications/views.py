
from django import http


from django.views import View

from E_business_project.settings.dev import logger
from apps.verifications import constants
from utils.response_code import RETCODE


class ImageCodeView(View):

    def get(self, request, uuid):
        """
         :param request: 请求对象
         :param uuid: 唯一标识图形验证码所属于的用户
         :return: image/jpg
         """
        # 生成图片验证码
        from libs.captcha.captcha import captcha
        text, image = captcha.generate_captcha()

        # 保存验证码
        from django_redis import get_redis_connection
        redis_client = get_redis_connection('verify_image_code')
        redis_client.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        return http.HttpResponse(image, content_type='image/jpg')

class SMSCodeView(View):

    def get(self, request, mobile):
        '''短信验证码逻辑实现'''

        # 1.解析校验参数--mobile 不用校验
        uuid = request.GET.get('image_code_id')
        image_code = request.GET.get('image_code')

        # 2.校验图形验证码 如果正确 发送验证码, 不正确 直接返回

        # 根据uuid 去redis数据库查询 图片验证码
        from django_redis import get_redis_connection
        image_redis_client = get_redis_connection('verify_image_code')
        redis_img_code  = image_redis_client.get('img_%s' % uuid)

        # 判断数据库中是否有数据
        if redis_img_code is None:
            return http.JsonResponse({'code': "4001", 'errmsg': '图形验证码失效了'})

        # 有值则删除
        try:
            image_redis_client.delete('img_%s' % uuid)
        except Exception  as e:
            logger.error(e)

        # 判断前端数据与redis数据库中数据是否相符
        if image_code.lower() != redis_img_code.decode().lower():
            return http.JsonResponse({'code': "4001", 'errmsg': '输入图形验证码有误'})

        # 生成短信验证码 保存验证码
        from random import randint
        sms_code = "%06d" % randint(0, 999999)
        sms_redis_client = get_redis_connection('sms_code')


        send_flag = sms_redis_client.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})

        # 创建管道
        pl = sms_redis_client.pipeline()
        # 保存短信验证码
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 重新写入send_flag
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()

        # 第三方发送短信验证码
        from celery_tasks.sms.tasks import ccp_send_sms_code
        send_result = ccp_send_sms_code(mobile, sms_code)
        print("当前验证码是:", sms_code)
        if send_result != 0:
            return http.HttpResponse({'code': '4001', 'errmsg': '发送短信失败'})

        return http.HttpResponse({'code':'0', 'errmsg': '发送短信成功'})








