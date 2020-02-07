from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from E_business_project.settings.dev import logger
from utils.response_code import RETCODE
from .models import Area


class AreasView(View):
    '''省市区数据展示'''

    def get(self, request):
        """提供省市区数据"""
        area_id = request.GET.get('area_id')

        if not area_id:
            '''提供省数据'''
            try:
                province_model_list = Area.objects.filter(parent__isnull=True)

                province_list = []
                for province_model in province_model_list:
                    province_list.append({'id': province_model.id, 'name': province_model.name})
            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '省份数据错误'})

            # 响应省份数据
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})
        else:
            # 提供市区数据
            try:
                parent_model = Area.objects.get(id=area_id)  # 查询市或区的父级
                sub_model_list = parent_model.subs.all()

                # 序列化市或区数据
                sub_list = []
                for sub_model in sub_model_list:
                    sub_list.append({'id': sub_model.id, 'name': sub_model.name})

                sub_data = {
                    'id': parent_model.id,  # 父级pk
                    'name': parent_model.name,  # 父级name
                    'subs': sub_list  # 父级的子集
                }
            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '城市或区数据错误'})

            # 响应市或区数据
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'sub_data': sub_data})

