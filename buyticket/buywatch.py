# coding=utf8

import time
from django.utils import timezone
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buyticket.settings")
django.setup()
from usermain.models import Buy


def watch():
    filltertime = timezone.now()-timezone.timedelta(minutes=15)
    buys = Buy.objects.filter(buy_time__lt=filltertime, buy_status=0).order_by('buy_time')
    for buy in buys:
        print(buy.delete())

if __name__ == '__main__':
    while True:
        watch()
        print("持续监控订单中...")
        time.sleep(60)