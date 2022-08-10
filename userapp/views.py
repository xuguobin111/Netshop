from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.views import View

from cartapp.cartmanager import SessionCartManager
from userapp.models import UserInfo,Area,Address
import jsonpickle

# Create your views here.
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        account=request.POST.get('account')
        pwd=request.POST.get('password')
        user=UserInfo.objects.create(uname=account,pwd=pwd)
        if user:
            request.session['user']=jsonpickle.dumps(user)
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/register/')


class CenterView(View):
    def get(self,request):
        return render(request,'center.html')


class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{'redirect':request.GET.get('redirct',''),'cartitems':request.GET.get('cartitems','')})
    def post(self,request):
        uname=request.POST.get('account','')
        pwd=request.POST.get('password','')
        redirect=request.POST.get('redirect','')
        useList=UserInfo.objects.filter(uname=uname,pwd=pwd)
        if useList:
            request.session['user']=jsonpickle.dumps(useList[0])
            # 将session中的购物项转移到数据库表中
            SessionCartManager(request.session).migrateSession2DB()
            if redirect == 'cart':
                return HttpResponseRedirect('/cart/queryAll/')
            elif redirect == 'order':
                return HttpResponseRedirect('/order/toOrder/?cartitems='+request.POST.get('cartitems',''))
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')

from utils.code import *
class loadCodeView(View):
    def get(self,request):
        img,txt=gene_code()
        #将txt保存到session
        request.session['sessionCode']=txt
        #响应页面
        return HttpResponse(img,content_type='image/png')


class CheckCodeView(View):
    def get(self,request):
        code=request.GET.get('code','')
        #获取系统生成的验证码
        sessioncode=request.session.get('sessionCode')
        flag=code==sessioncode
        return JsonResponse({'flag':flag})


class LogoutView(View):
    def get(self,request):
        request.session.clear()
        return JsonResponse({'flag':True})


class AddressView(View):
    def get(self,request):
        user =jsonpickle.loads(request.session.get('user'))
        addrList = user.address_set.all()
        return render(request,'address.html',{'addrList':addrList})

    def post(self,request):
        params = request.POST.dict()
        params.pop('csrfmiddlewaretoken')
        #获取当前用户登录对象
        user=jsonpickle.loads(request.session.get('user'))
        Address.objects.create(userinfo=user,isdefault=(lambda count:True if count==0 else False)(user.address_set.count()),**params)
        return HttpResponseRedirect('/user/address/')
from django.core.serializers import serialize
def loadAddrView(request):
    pid=request.GET.get('pid',-1)
    pid=int(pid)
    #根据父Id查询区划信息
    areaList = Area.objects.filter(parentid=pid)
    #序列化areaList
    jareaList=serialize('json',areaList)
    return JsonResponse({'jareaList': jareaList})