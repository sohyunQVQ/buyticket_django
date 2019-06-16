from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from usermain.models import Car, Buy
from django.utils import timezone
from django.core import serializers
import json

# Create your views here.

def index(requsts):

    title = "主页"

    return render(requsts, 'index.html',{'title':title})

def choose(requsts):
    returnmsg=""
    now = timezone.now()
    if requsts.method == 'POST':
        user_name=requsts.POST['user_name']
        user_phone=requsts.POST['user_phone']
        user_key=requsts.POST['user_key']
        car_id=requsts.POST['car_id']
        if user_name!="" and user_phone !="" and user_key!="" and car_id!="":
            car = Car.objects.filter(id=car_id).first()
            if car.seat_number <=0:
                returnmsg = "已没有座位, 请选择其他车辆"
            else:
                buy = Buy.objects.get_or_create(car_id=car_id, user_name=user_name, user_phone=user_phone,user_key=user_key,buy_price=car.price, buy_time=now)
                if buy:
                    car.seat_number = car.seat_number-1
                    car.save()
                    returnmsg = "提交成功,请牢记暗号后面以此为凭证"
                else:
                    returnmsg = "请勿重复提交信息"
        else:
            returnmsg = "请完整填写, 内容都是必填项"

    data = {}
    cars = Car.objects.filter(start_time__gt=now).order_by('start_time')
    if len(cars):
        data['data'] = json.loads(serializers.serialize("json", cars))
        cardata = data
    else:
        cardata=""
    return render(requsts, 'choose.html',{'title':"车票预定",'cardata':cardata,'returnmsg':returnmsg})

def select(requsts):
    data = {}
    now = timezone.now()
    cars = Car.objects.filter(start_time__gt=now).order_by('start_time')
    data['data'] = json.loads(serializers.serialize("json", cars))
    cardata = data
    return render(requsts, 'select.html',{'title':"车票查询",'cardata':cardata})

def query(requsts):
    now = timezone.now()
    order = {}
    order['requests']='GET'
    if requsts.method == 'POST':
        key = requsts.POST['key']
        order['requests']='POST'
        buy = Buy.objects.filter(user_key=key)
        if len(buy)!=0:
            car = Car.objects.filter(id=buy.first().car_id).first()
            order['time']=buy.first().buy_time
            if buy.first().buy_status == 0:
                order['status']='未支付'
            else:
                order['status']='已支付'
                order['statusnumber']=1
            if car.car_id!='暂无':
                order['car'] = car.car_id
            order['starttime']=car.start_time
            return render(requsts, 'query.html', {'title': "车票进度查询",'order':order})
    return render(requsts, 'query.html', {'title': "车票进度查询",'order':order})

def pay(requsts):

    return render(requsts, 'pay.html',{'title':"支付"})


def api(requsts):

    type = requsts.GET['type']


    return HttpResponse("")