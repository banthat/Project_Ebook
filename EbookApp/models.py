from django.db import models
import datetime
from django.db.models import F, Sum, Count
# Create your models here.

# หมวดหมู่หนังสือ
class Category(models.Model):
    name = models.CharField(max_length=50, default="")
    type = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.id) + ":" + self.name + ":" + self.type

    def getCountEbook(self):
        count = Ebook.objects.filter(category=self).aggregate(count=Count('bid'))
        return count['count']

    def getCountEbooks(self):
        category = Category.objects.annotate(number_of_ebook=Count('ebook'))

# นักเขียน
class Writer(models.Model):
    wid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=100, default="")
    publisher = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.wid + ":" + self.name

    def getCountEbook(self):
        count = Ebook.objects.filter(writer=self).aggregate(count=Count('bid'))
        return count['count']

    def getCountEbooks(self):
        writer = Writer.objects.annotate(number_of_ebook=Count('ebook'))

# หนังสือ
class Ebook(models.Model):
    bid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    price = models.FloatField(default=0.00)
    sellDate = models.DateField(default=None)
    picture = models.ImageField(upload_to='static/ebook/', default="")
    net = models.IntegerField(default=0)
    desc = models.TextField(max_length=5000, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.bid + ":" + self.name + ", " + str(self.price)

    def getCountOrder(self):
        count = OrderDetails.objects.filter(ebook=self).aggregate(count=Count('id'))
        return count['count']

    def getSaleAmount(self):
        amount = Samplesale.objects.filter(ebook=self).aggregate(amount=Sum(F('amount')))
        return amount['amount']

# พนักงาน
class Employee(models.Model):
    eid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    position = models.CharField(max_length=50, default="")
    telephone = models.CharField(max_length=10, default='')
    password = models.CharField(max_length=255, default="12345678")

    def __str__(self):
        return self.eid + ":" + self.name + ", " + self.position

    def getCountConfirm(self):
        count = Confirms.objects.filter(employee=self).aggregate(count=Count('id'))
        return count['count']

    def getCountAccept(self):
        count = Accepts.objects.filter(employee=self).aggregate(count=Count('id'))
        return count['count']

    def getCountSend(self): #การส่งสินค้า
        count = Send.objects.filter(employee=self).aggregate(count=Count('id'))
        return count['count']

# ลูกค้า
class Customers(models.Model):
    cid = models.CharField(max_length=13, primary_key=True, default='')
    name = models.CharField(max_length=100, default='')
    address = models.TextField(max_length=400, default="")
    telephone = models.CharField(max_length=10, default='')
    password = models.CharField(max_length=8, default="12345678")

    def __str__(self):
        return self.cid + " : " + self.name

class Orders(models.Model):
    oid = models.CharField(max_length=13, primary_key=True, default="")
    odate = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=1, default="")
    def __str__(self):
        return self.oid + " " + str(self.odate.strftime("%Y-%m-%d")) + " : " + self.customer.name + ", " + self.getStatus()
        # return self.oid + " " + str(self.odate.strftime("%Y-%m-%d")) + " : " + self.customer.name + ", " + str(self.getTotal()) + ", " + self.getStatus()

    def newOrderId(self):
        #ord-yymm-xxxxxx ทำหมายเลขใบสั่งซื้ออัตโนมัติ
        yy = str(datetime.date.today().strftime('%y'))
        mm = str(datetime.date.today().strftime('%m'))
        lastOrder = Orders.objects.last()
        if lastOrder:
            lastId = int(lastOrder.oid[9:])
        else:
            lastId = 0
        id = str(lastId+1)
        id = id.zfill(6)
        newId = "OD-" + yy + mm + id
        self.oid = newId

    def getStatus(self):
        if self.status == '1':
            return 'รอการยืนยัน'
        elif self.status == '2':
            return 'รอการชำระเงิน'
        elif self.status == '3':
            return 'รอยืนยันการชำระเงิน'
        elif self.status == '4':
            return 'รอสินค้าส่ง'
        elif self.status == '5':
            return 'สำเร็จ'
        elif self.status == '6':
            return 'ยกเลิกการสั่งซื้อ'
        elif self.status == '7':
            return 'ปฎิเสธคำสั่งซื้อ'

    def getOrderDetails(self):
        orderDetails = OrderDetails.objects.filter(order=self)
        return orderDetails

    def getTotal(self):
        total = OrderDetails.objects.filter(order=self).aggregate(total=Sum(F('oprice') * F('quantity')))
        return total['total']

    def getCount(self):
        count = OrderDetails.objects.filter(order=self).aggregate(count=Count('id'))
        return count['count']

class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    ebooks = models.ForeignKey(Ebook, on_delete=models.CASCADE, default=None)
    oprice = models.FloatField(default=0.00)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.order.oid + " : " + self.ebooks.bid + " " + self.ebooks.name + ", " + str(self.quantity)

    def getTotal(self):
        return self.oprice * self.quantity

class Transfers(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    tdate = models.DateTimeField(auto_now_add = True)
    reference = models.CharField(max_length=35, default="")
    bank = models.CharField(max_length=50, default="")
    bill = models.ImageField(upload_to='static/bills/', default="")
    comment = models.CharField(max_length=200, default="")

class Confirms(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=None)
    cdate = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200, default="")

class Accepts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=None)
    adate = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200, default="")

class Send(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=None)
    sdate = models.DateTimeField(auto_now_add = True)
    company = models.CharField(max_length=50, default="")
    tag = models.CharField(max_length=50, default="")
    comment = models.CharField(max_length=200, default="")

class Cancel(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    cdate = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, default="")

class Reject(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=None)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=None)
    rdate = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, default="")

class Samplesale(models.Model): # ตารางสมมุติ เอาไว้เก็บยอดขาย เพื่อเอาไปทำ Dashboard
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, default=None)
    datesale = models.DateField(default=None)
    amount = models.IntegerField(default=0)  #ยอดขาย

    def __str__(self):
        return "Hey: " + str(self.id) + ":" + self.ebook.name + ", " + str(self.datesale.year) + ", " + str(self.amount)
