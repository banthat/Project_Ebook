from django.contrib import admin
from EbookApp.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Writer)
admin.site.register(Ebook)
admin.site.register(Employee)
admin.site.register(Customers)
admin.site.register(Orders)
admin.site.register(OrderDetails)
admin.site.register(Accepts)
admin.site.register(Transfers)
admin.site.register(Confirms)
admin.site.register(Send)
admin.site.register(Cancel)
admin.site.register(Reject)

