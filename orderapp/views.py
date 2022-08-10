import datetime
import uuid

from django.shortcuts import render,HttpResponseRedirect,HttpResponse
import jsonpickle
# Create your views here.
from cartapp.cartmanager import getCartManger
from orderapp.models import Order, OrderItem
from userapp.models import Address
from utils.alipay import AliPay
from goodsapp.models import Inventory
from django.db.models import F



#创建alipay对象
alipayObj=AliPay(appid='2021003142617213',app_notify_url='http://127.0.0.1:8000/order/checkPay',app_private_key_path='orderapp/keys/my_private_key.txt',
                 alipay_public_key_path='orderapp/keys/alipay_public_key.txt',return_url='http://127.0.0.1:8000/order/checkPay',
                 debug=True)
def order_view(request):
    #获取请求参数
    cartitems = request.GET.get('cartitems','')

    #获取当前用户登录信息
    user = request.session.get('user','')

    #判断用户是否登录
    if not user:
        return HttpResponseRedirect('/user/login/?redirct=order&cartitems='+cartitems)

    return HttpResponseRedirect('/order/toOrder/?cartitems='+cartitems)


def toOrder(request):

    #接收请求参数
    cartitems = request.GET.get('cartitems','')

    #将cartitems进行反序列化
    cartitemsList = jsonpickle.loads(cartitems)

    cartItemObjList = [getCartManger(request).get_cartitems(**ci) for ci in cartitemsList if ci]

    #获取用户的默认收件地址
    user = jsonpickle.loads(request.session.get('user'))
    addr = user.address_set.get(isdefault=True)

    #支付总金额
    totalPrice = 0
    for cio in cartItemObjList:
        totalPrice += cio.getTotalPrice()

    return render(request,'order.html',{'cartitemList':cartItemObjList,'addr':addr,'totalPrice':totalPrice})


def toPay(request):
    #接收请求参数
    aid = request.GET.get('address',-1)
    aid = int(aid)
    addrObj = Address.objects.get(id=aid)


    payway = request.GET.get('payway','')

    cartitems = request.GET.get('cartitems','')

    cartitemList = jsonpickle.loads(cartitems)


    #添加Order表信息

    params = {
        'out_trade_num':uuid.uuid4().hex,
        'order_num':datetime.datetime.today().strftime('%Y%m%d%H%M%S'),
        'payway':payway,
        'address':addrObj,
        'user':jsonpickle.loads(request.session.get('user'))
    }

    orderObj = Order.objects.create(**params)

    #添加OrderItem表信息

    orderItemList = [OrderItem.objects.create(order=orderObj,**ci) for ci in cartitemList if ci]

    #获取支付总金额
    totalPrice = request.GET.get('totalPrice')
    alipayParams = alipayObj.direct_pay(subject=u'天猫超市', out_trade_no=orderObj.out_trade_num, total_amount=str(totalPrice))

    url = alipayObj.gateway+'?'+alipayParams

    return HttpResponseRedirect(url)


def checkPay(request):

    #获取请求参数
    params = request.GET.dict()
    print(params)

    #获取签名
    sign = params.pop('sign')

    #获取当前登录用户对象
    user = jsonpickle.loads(request.session.get('user'))

    #判断是否支付成功
    if alipayObj.verify(params,sign):
        #修改订单信息
        out_trade_no = params.get('out_trade_no')
        trade_num = params.get('trade_no','')
        order = Order.objects.get(out_trade_num=out_trade_no)
        order.status = u'待发货'
        order.trade_no = trade_num
        order.save()

        #修改库存信息
        orderItemList = order.orderitem_set.all()
        [Inventory.objects.filter(goods_id=oi.goodsid,color_id=oi.colorid,size_id=oi.sizeid).update(count=F('count')-oi.count) for oi in orderItemList if oi]

        #清空购物车
        [user.cartitem_set.filter(goodsid=oi.goodsid,colorid=oi.colorid,sizeid=oi.sizeid).delete() for oi in orderItemList if oi]



        return HttpResponse('支付成功！')

    return HttpResponse('支付失败！')