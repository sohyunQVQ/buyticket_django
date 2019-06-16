from django.db import models

# Create your models here.


class Car(models.Model):
    car_id = models.CharField(max_length=10, verbose_name="车牌号(可填暂无)") #车牌信息
    route_left =  models.CharField(max_length=50, verbose_name="出发地点") #出发点
    route_mid =  models.CharField(max_length=50, null=True,blank=True,verbose_name="经过点(可不填)") #经过点
    route_right =  models.CharField(max_length=50,verbose_name="终点站") #终点
    start_time =  models.DateTimeField(verbose_name="出发时间") #出发时间
    seat_number = models.IntegerField(verbose_name="座位数量") #座位数量
    price = models.FloatField(verbose_name="价格") #价格

    def __str__(self):
        return self.car_id

class Buy(models.Model):
    car_id = models.IntegerField(verbose_name="车Id")
    user_name =models.CharField(max_length=12,verbose_name="联系人")
    user_phone = models.CharField(max_length=11,verbose_name="手机号码")
    user_key = models.CharField(max_length=50,verbose_name="暗号")
    buy_price = models.FloatField(verbose_name="需支付金额", default=0)
    buy_time =  models.DateTimeField(verbose_name="提交时间")
    buy_status = models.IntegerField(verbose_name="状态",default=0) #1为已经支付 #2过期(过期的时候把金额修改为999)
    def __str__(self):
        return self.user_name

class Pay(models.Model):
    buy_id = models.CharField(max_length=10,verbose_name="下单Id")
    wechat_id = models.CharField(max_length=50,verbose_name="支付微信号")
    pay_money = models.CharField(max_length=10,verbose_name="支付金额")
    pay_time = models.CharField(max_length=50,verbose_name="提交时间")
    pay_key = models.CharField(max_length=50,verbose_name="支付暗号(备注)")
    def __str__(self):
        return self.buy_id