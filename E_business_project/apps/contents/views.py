from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.contents.models import ContentCategory


class IndexView(View):
    '''首页广告'''

    def get(self, request):
        '''广告首页'''

        # 查询商品频道和分类
        from .utils import get_categories
        categories = get_categories()

        # 广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories':categories,
            'contents': contents,
        }

        # 查询商品频道和分类
        return render(request, 'index.html', context=context)