from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):

    def get(self, request):
        '''广告首页'''
        return render(request, 'index.html')