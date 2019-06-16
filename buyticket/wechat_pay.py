#coding=utf8
import itchat
from itchat.content import *
import re
import time
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buyticket.settings")
django.setup()

from usermain.models import Pay, Buy

def save_model(returnmsg):
	print("=========%s=========" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	pay = Pay(buy_id=123, wechat_id=returnmsg['fromuser'], pay_money=returnmsg['money'], pay_time=returnmsg['createtime'],
			  pay_key=returnmsg['note'])
	pay.save()
	print("微信收款：%s元,备注内容：%s" % (returnmsg['money'], returnmsg['note']))
	buys = Buy.objects.filter(user_key=returnmsg['note']).order_by('buy_time')
	for buy in buys:
		buymoney = format(buy.buy_price,'.2f')
		if buymoney==returnmsg['money']:
			buy.buy_status = 1
			buy.save()
			print("已经修改支付状态\n")
			break
	print("没有发现合适的备注内容\n")

@itchat.msg_register([SHARING])
def text_reply(msg):
	returnmsg = {}
	returnmsg['content'] = msg.Content
	try:
		returnmsg['fromuser'] = msg.FromUserName
		returnmsg['money'] = re.findall(re.compile(r'微信支付收款(.*?)元'), returnmsg['content'])[0]
		returnmsg['createtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		returnmsg['note'] = re.findall(re.compile(r'付款方备注(.*?)\n'), returnmsg['content'])[0]
	except IndexError:
		returnmsg['note'] = ""
	if returnmsg['note'] and returnmsg['money']:
		save_model(returnmsg)

if __name__ == '__main__':
	itchat.auto_login(True)
	itchat.run()