from django.contrib import admin

from .models import cheque_details,cheque_deposit


admin.site.register(cheque_details)
admin.site.register(cheque_deposit)

# Register your models here.