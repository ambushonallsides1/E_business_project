from django.conf.urls import url

from . import views

urlpatterns = [
    # 省市区地址显示
    url(r'^areas/$', views.AreasView.as_view()),
]
