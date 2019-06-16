from django.contrib import admin
from .models import Car,Buy,Pay
# Register your models here.

admin.site.register(Buy)
admin.site.register(Car)
admin.site.register(Pay)