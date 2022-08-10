from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views import View
# Create your views here.
from cartapp.cartmanager import *


class CartView(View):
    def post(self,request):
        request.session.modified = True
        flag=request.POST.get('flag','')
        if flag == 'add':
            #获取cartManager对象
            cartManager = getCartManger(request)
            #加入购物车操作
            cartManager.add(**request.POST.dict())
        elif flag == 'plus':
            cartManager = getCartManger(request)
            cartManager.update(step=1,**request.POST.dict())
        elif flag == 'minus':
            cartManager = getCartManger(request)
            cartManager.update(step=-1,**request.POST.dict())
        elif flag =='delete':
            cartManager = getCartManger(request)
            cartManager.delete(**request.POST.dict())
        return HttpResponseRedirect('/cart/queryAll')


def queryAll(request):
    cartManager = getCartManger(request)
    cartItemList = cartManager.queryAll()
    return render(request,'cart.html',{'cartItemList':cartItemList})