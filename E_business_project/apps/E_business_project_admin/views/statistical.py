from datetime import date
from apps.users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


class UserTotalCountView(APIView):
    '''用户总量统计'''
    # 管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取所有用户总数
        count = User.objects.all().count()
        return Response({
            'count': count,
            'date': now_date
        })


class UserDailyCountView(APIView):
    '''日增用户统计'''
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取日增用户总数
        count = User.objects.filter(date_joined__gte=now_date).count()
        return Response({
            'count': count,
            'date': now_date
        })


class UserDailyActiveCountView(APIView):
    '''日活跃用户统计'''
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取活跃用户总数
        count = User.objects.filter(last_login__gte=now_date).count()
        return Response({
            'count': count,
            'date': now_date
        })


class UserDailyOrderCountView(APIView):
    '''日下单用户量统计'''
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取当日下单用户数量  orders__create_time 订单创建时间
        count = User.objects.filter(orderinfo__create_time__gte=now_date).count()
        return Response({
            "count": count,
            "date": now_date
        })


from datetime import timedelta


class UserMonthCountView(APIView):
    '''月增用户统计'''
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取一个月前日期
        start_date = now_date - timedelta(days=30)
        # 创建空列表保存每天的用户量
        date_list = []

        for i in range(30):
            # 循环遍历获取当天日期
            index_date = start_date + timedelta(days=i)
            # 指定下一天日期
            cur_date = start_date + timedelta(days=i + 1)

            # 查询条件是大于当前日期index_date，小于明天日期的用户cur_date，得到当天用户量
            count = User.objects.filter(date_joined__gte=index_date, date_joined__lt=cur_date).count()

            date_list.append({
                'count': count,
                'date': index_date
            })

        return Response(date_list)


from apps.goods.models import GoodsVisitCount
from apps.E_business_project_admin.serializers.statistical import UserCategoryCountSerializer


class UserCategoryCountAPIView(APIView):
    '''日分类商品访问量'''
    # 添加权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当天日期
        today = date.today()

        # 查询数据
        data = GoodsVisitCount.objects.filter(date__gte=today)

        serializer = UserCategoryCountSerializer(data, many=True)

        return Response(serializer.data)
