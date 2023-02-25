from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from EbookApp.forms import *
import datetime, os
from django.db.models import Q
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger,)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# ยังไม่ล็อคอิน เป็นภายใน
def chkPermission(request):
    # กรณีล็อคอิน
    if 'userStatus' in request.session:
        userStatus = request.session['userStatus']
        # ถ้าเป็นลูกค้า ไม่ให้ใช้
        if userStatus == 'customer':
            messages.add_message(request, messages.WARNING, "ท่านกำลังเข้าใช้ในส่วนที่ไม่ได้รับอนุญาต!!!")
            return False
        else:
            return True
    # กรณียังไม่ล็อคอิน
    # else:
    #     if Employee.objects.count() != 0:
    #         messages.add_message(request, messages.WARNING, "ท่านกำลังเข้าใช้ในส่วนที่ไม่ได้รับอนุญาต!!!")
    #         return False
    #     else:
    #         return True

# Create your views here.
def home(request):
    countEmp = Employee.objects.count()
    print("countEmp:" + str(countEmp))
    if countEmp == 0:
        messages.add_message(request, messages.INFO, "เพิ่มข้อมูลพนักงาน สำหรับการเข้าใช้ครั้งแรก")
        return redirect('employeeNew')
    else:
        return render(request, 'home.html')

@login_required(login_url='userAuthen')
def categoryList(request):
    if not chkPermission(request):
        return redirect('home')
    category = Category.objects.all().order_by('id')
    context = {'category': category}
    return render(request, 'Category/categoryList.html', context)

@login_required(login_url='userAuthen')
def categoryNew(request):
    if not chkPermission(request):
        return redirect('home')
    if request.method == 'POST':
        form = CategoryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categoryList')
        else:
            context = {'form': form}
            return render(request, 'Category/categoryNew.html', context)
    else:
        form = CategoryForm()
        context = {'form': form}
        return render(request, 'Category/categoryNew.html', context)

@login_required(login_url='userAuthen')
def categoryUpdate(request, id):
    if not chkPermission(request):
        return redirect('home')
    category = get_object_or_404(Category, id=id)
    form = CategoryForm(data=request.POST or None, instance=category)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('categoryList')
        else:
            context = {'form': form}
            return render(request, 'Category/categoryUpdate.html', context)
    else:
        context = {'form': form}
        return render(request, 'Category/categoryUpdate.html', context)

@login_required(login_url='userAuthen')
def categoryDelete(request, id):
    if not chkPermission(request):
        return redirect('home')
    category = get_object_or_404(Category, id=id)
    form = CategoryForm(data=request.POST or None, instance=category)
    if request.method == 'POST':
        category.delete()
        return redirect('categoryList')
    else:
        form.deleteForm()
        context = {'form': form, 'category': category}
        return render(request, 'Category/categoryDelete.html', context)

@login_required(login_url='userAuthen')
def writerList(request):
    if not chkPermission(request):
        return redirect('home')
    writer = Writer.objects.all()
    context = {'writer': writer}
    return render(request, 'Writer/writerList.html', context)

@login_required(login_url='userAuthen')
def writerNew(request):
    if not chkPermission(request):
        return redirect('home')
    context = {}
    if request.method == "POST":
        form = WriterForm(data=request.POST, files=request.FILES)
        obj = Writer.objects.filter(wid=request.POST['wid'])
        if obj:
            messages.add_message(request, messages.WARNING, 'รหัสสินค้าซ้ำกับกับที่มีอยู่แล้ว')
            context["form"] = form
            return render(request, 'Writer/writerNew.html', context)
        elif form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลสินค้าสำเร็จแล้ว')
            return redirect('writerList')
        else:
            messages.add_message(request, messages.WARNING, 'ข้อมูลไม่ถูกต้อง/ไม่สมบูรณ์ ไม่สามารถบันทึกได้')
            return redirect('writerList')
    else:
        form = WriterForm()
        context = {'form': form}
        return render(request, 'Writer/writerNew.html', context)

@login_required(login_url='userAuthen')
def writerUpdate(request, wid):
    if not chkPermission(request):
        return redirect('home')
    writer = get_object_or_404(Writer, wid=wid)
    form = WriterForm(data=request.POST or None, instance=writer)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('writerList')
        else:
            context = {'form': form}
            return render(request, 'Writer/writerUpdate.html', context)
    else:
        context = {'form': form}
        return render(request, 'Writer/writerUpdate.html', context)

@login_required(login_url='userAuthen')
def writerDelete(request, wid):
    if not chkPermission(request):
        return redirect('home')
    writer = get_object_or_404(Writer, wid=wid)
    form = WriterForm(data=request.POST or None, instance=writer)
    if request.method == 'POST':
        writer.delete()
        return redirect('writerList')
    else:
        form.deleteForm()
        context = {'form': form, 'writer': writer}
        return render(request, 'Writer/writerDelete.html', context)

@login_required(login_url='userAuthen')
def ebookList(request):
    if not chkPermission(request):
        return redirect('home')
    ebook = Ebook.objects.all()
    context = {'ebook': ebook}
    return render(request, 'Ebook/ebookList.html', context)

@login_required(login_url='userAuthen')
def ebookNew(request):
    if not chkPermission(request):
        return redirect('home')
    if request.method == 'POST':
        form = EbookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            bid = newForm.bid
            filepath = newForm.picture.name
            point = filepath.rfind('.')
            ext = filepath[point:]
            filenames = filepath.split('/')
            filename = filenames[len(filenames)-1]
            newfilename = bid + ext
            newForm.save()
            ebook = get_object_or_404(Ebook, bid=bid)
            ebook.picture.name = '/ebook/' + newfilename
            ebook.save()
            if os.path.exists('static/ebook/' + newfilename):
                os.remove('static/ebook/' + newfilename)
            os.rename('static/ebook/' + filename, 'static/ebook/' + newfilename)
        else:
            ebook = get_object_or_404(Ebook, bid=request.POST['bid'])
            if ebook:
                messages.add_message(request, messages.WARNING, "รหัสสินค้าซ้ำกับที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'Ebook/ebookNew.html', context)
        return redirect('ebookList')
    else:
        form = EbookForm()
        context = {'form': form}
        return render(request, 'Ebook/ebookNew.html', context)

@login_required(login_url='userAuthen')
def ebookUpdate(request, bid):
    if not chkPermission(request):
        return redirect('home')
    ebook = get_object_or_404(Ebook, bid=bid)
    picture = ebook.picture.name
    if request.method == 'POST':
        form = EbookForm(request.POST or None, instance=ebook, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            bid = newForm.bid
            print(newForm.picture.name)
            if newForm.picture.name != picture:
                newForm.save()
                filepath = newForm.picture.name
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = filenames[len(filenames) - 1]
                newfilename = bid + ext
                ebook = get_object_or_404(Ebook, bid=bid)
                ebook.picture.name = '/ebook/' + newfilename
                ebook.save()
                if os.path.exists('static/ebook/' + newfilename):
                    os.remove('static/ebook/' + newfilename)
                os.rename('static/ebook/' + filename, 'static/ebook/' + newfilename)
            else:
                newForm.save()
        return redirect('ebookList')
    else:
        form = EbookForm(instance=ebook)
        form.updateForm()
        context = {'form': form}
        return render(request, 'Ebook/ebookUpdate.html', context)

@login_required(login_url='userAuthen')
def ebookDelete(request, bid):
    if not chkPermission(request):
        return redirect('home')
    ebook = get_object_or_404(Ebook, bid=bid)
    picture = ebook.picture.name
    # form = EbookForm(data=request.POST or None, instance=ebook)
    if request.method == 'POST':
        ebook.delete()
        if os.path.exists('static' + picture):
            os.remove('static' + picture)
        return redirect('ebookList')
    else:
        form = EbookForm(instance=ebook)
        form.deleteForm()
        context = {'form': form, 'ebook': ebook}
        return render(request, 'Ebook/ebookDelete.html', context)

@login_required(login_url='userAuthen')
def employeeList(request):
    if not chkPermission(request):
        return redirect('home')
    employee = Employee.objects.all().exclude(Q(position='Administrator')).order_by('eid')
    context = {'employee': employee}
    return render(request, 'Employee/employeeList.html', context)

# @login_required(login_url='userAuthen')
def employeeNew(request):
    if not chkPermission(request):
        return redirect('home')
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            # สร้าง user ในระบบ authen ของ Django ---
            # eid = request.POST['eid']
            # name = request.POST['name']
            # email = 'none@gmail.com'
            # password = request.POST['password']
            # user = User.objects.create_user(eid, email, password)
            # user.first_name = name
            # user.is_staff = True
            # user.save()
            return redirect('employeeList')
        else:
            context = {'form': form}
            return render(request, 'Employee/employeeNew.html', context)
    else:
        form = EmployeeForm()
        context = {'form': form}
        return render(request, 'Employee/employeeNew.html', context)

@login_required(login_url='userAuthen')
def employeeUpdate(request, eid):
    if not chkPermission(request):
        return redirect('home')
    employee = get_object_or_404(Employee, eid=eid)
    if request.method == 'POST':
        form = EmployeeForm(request.POST or None, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employeeList')
        else:
            context = {'form': form}
            return render(request, 'Employee/employeeUpdate.html', context)
    else:
        form = EmployeeForm(instance=employee)
        form.updateForm()
        context = {'form': form}
        return render(request, 'Employee/employeeUpdate.html', context)

@login_required(login_url='userAuthen')
def employeeDelete(request, eid):
    if not chkPermission(request):
        return redirect('home')
    employee = get_object_or_404(Employee, eid=eid)
    if request.method == 'POST':
        employee.delete()
        return redirect('employeeList')
    else:
        form = EmployeeForm(instance=employee)
        form.deleteForm()
        context = {'form': form, 'employee': employee}
        return render(request, 'Employee/employeeDelete.html', context)

@login_required(login_url='userAuthen')
def customerList(request):
    if not chkPermission(request):
        return redirect('home')
    customers = Customers.objects.all().order_by('cid')
    context = {'customers': customers}
    return render(request, 'Customer/customerList.html', context)

def customerRegister(request):
    if request.method == 'POST':
        form = CustomersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userAuthen')
        else:
            context = {'form': form}
            return render(request, 'Customer/customerRegister.html', context)
    else:
        form = CustomersForm()
        context = {'form': form}
        return render(request, 'Customer/customerRegister.html', context)

def customerUpdate(request, cid):
    customer = get_object_or_404(Customers, cid=cid)
    if request.method == 'POST':
        form = CustomersForm(request.POST or None, instance=customer)
        if form.is_valid():
            form.save()
            if request.session.get('userStatus') == 'customer':
                return redirect('home')
            else:
                return redirect('customerList')
        else:
            context = {'form': form}
            return render(request, 'Customer/customerUpdate.html', context)
    else:
        form = CustomersForm(instance=customer)
        form.updateForm()
        context = {'form': form}
        return render(request, 'Customer/customerUpdate.html', context)

def userChangePassword(request):
    userId = request.session.get('userId')
    user = None
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST or None)
        if request.session.get('userStatus') == 'customer':
            user = get_object_or_404(Customers, cid=userId)
        else:
            user = get_object_or_404(Employee, eid=userId)
        context = {'form': form}
        if request.POST['oldPassword'] == user.password:
            if request.POST['newPassword'] == request.POST['confirmPassword']:
                user.password = request.POST['newPassword']
                user.save()
                messages.add_message(request, messages.INFO, "เปลี่ยนรหัสผ่านเสร็จเรียบร้อย...")
                return redirect('home')
            else:
                messages.add_message(request, messages.WARNING, "รหัสผ่านใหม่กับรหัสที่ยืนยันไม่ตรงกัน...")
                return render(request, 'userChangePassword.html', context)
        else:
            messages.add_message(request, messages.ERROR, "รหัสผ่านที่ระบุไม่ถูกต้อง...")
            return render(request, 'userChangePassword.html', context)
    else:
        form = ChangePasswordForm(initial={'userId': userId})
        context = {'form': form}
        return render(request, 'userChangePassword.html', context)

def userResetPassword(request, userId):
    user = None
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST or None)
        if request.session.get('userStatus') == 'customer':
            user = get_object_or_404(Customers, cid=userId)
        else:
            user = get_object_or_404(Employee, eid=userId)
        context = {'form': form}
        if request.POST['newPassword'] == request.POST['confirmPassword']:
            user.password = request.POST['newPassword']
            user.save()
            messages.add_message(request, messages.INFO, "เปลี่ยนรหัสผ่านเสร็จเรียบร้อย...")
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, "รหัสผ่านใหม่กับรหัสที่ยืนยันไม่ตรงกัน...")
            return render(request, 'userResetPassword.html', context)
    else:
        form = ResetPasswordForm(initial={'userId': userId})
        context = {'form': form}
        return render(request, 'userResetPassword.html', context)


def userAuthen(request):
    if request.method == 'POST':
        userName = request.POST.get("userName")
        userPass = request.POST.get("userPass")
        user = Customers.objects.filter(cid=userName).filter(password=userPass).first()
        # user = get_object_or_404(Customers, cid=userName, password=userPass)
        if user:
            request.session['userId'] = user.cid
            request.session['userName'] = user.name
            request.session['userStatus'] = 'customer'
            # messages.add_message(request, messages.INFO, "Login success..")
            if request.session.get('orderActive'):
                del request.session['orderActive']
                return redirect('checkout')
            else:
                return redirect('home')
        else:
            user = Employee.objects.filter(eid=userName).filter(password=userPass).first()
            if user:
                request.session['userId'] = user.eid
                request.session['userName'] = user.name
                request.session['userStatus'] = user.position
                # messages.add_message(request, messages.INFO, "Login success..")
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, "User or Password not Correct!!!..")
                data = {'userName': userName}
                return render(request, 'userAuthen.html', data)
    else:
        data = {'userName': ''}
        return render(request, 'userAuthen.html', data)

def userLogout(request):
    del request.session["userId"]
    del request.session["userName"]
    del request.session["userStatus"]
    return redirect('home')

def ebookShop(request):
    if request.method == 'POST':
        bid = request.POST.get('bid')
        qnt = int(request.POST.get('qnt'))
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(bid)
            if quantity:
                cart[bid] = quantity + qnt
            else:
                cart[bid] = qnt
        else:
            cart = {}
            cart[bid] = qnt
        request.session['cart'] = cart
        request.session['count'] = len(cart)
        return redirect('ebookShop')
    else:
        ebooks = Ebook.objects.all().order_by('bid')
        data = {'ebooks': ebooks}
        return render(request, 'Shop/ebookShop.html', data)

def ebook_1(request):
    if request.method == 'POST':
        bid = request.POST.get('bid')
        qnt = int(request.POST.get('qnt'))
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(bid)
            if quantity:
                cart[bid] = quantity + qnt
            else:
                cart[bid] = qnt
        else:
            cart = {}
            cart[bid] = qnt
        request.session['cart'] = cart
        request.session['count'] = len(cart)
        return redirect('ebook_1')
    else:
        ebooks = Ebook.objects.all().order_by('bid')
        data = {'ebooks': ebooks}
        return render(request, 'EbookShop/ebook_1.html', data)

def ebook_2(request):
    if request.method == 'POST':
        bid = request.POST.get('bid')
        qnt = int(request.POST.get('qnt'))
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(bid)
            if quantity:
                cart[bid] = quantity + qnt
            else:
                cart[bid] = qnt
        else:
            cart = {}
            cart[bid] = qnt
        request.session['cart'] = cart
        request.session['count'] = len(cart)
        return redirect('ebook_1')
    else:
        ebooks = Ebook.objects.all().order_by('bid')
        data = {'ebooks': ebooks}
        return render(request, 'EbookShop/ebook_2.html', data)

def ebook_3(request):
    if request.method == 'POST':
        bid = request.POST.get('bid')
        qnt = int(request.POST.get('qnt'))
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(bid)
            if quantity:
                cart[bid] = quantity + qnt
            else:
                cart[bid] = qnt
        else:
            cart = {}
            cart[bid] = qnt
        request.session['cart'] = cart
        request.session['count'] = len(cart)
        return redirect('ebook_3')
    else:
        ebooks = Ebook.objects.all().order_by('bid')
        data = {'ebooks': ebooks}
        return render(request, 'EbookShop/ebook_3.html', data)

def basket(request):
    cart = request.session.get('cart')
    if request.method == 'POST':
        action = request.POST.get('action')
        bid = request.POST.get('bid')
        qnt = int(request.POST.get('qnt'))
        if action == "Update": #กดปุ่ม Update
            if cart[bid]:
                cart[bid] = qnt
        else: # กดปุ่มลบ
            del cart[bid]
        request.session['cart'] = cart
        request.session['count'] = len(cart)
    if len(cart) == 0:
        del request.session['cart']
        del request.session['count']
        del request.session['sum']
        return redirect('ebookShop')

    cart = request.session.get('cart')
    items = []
    sum = 0.00
    for item in cart:
        ebooks = Ebook.objects.get(bid=item)
        total = ebooks.price * cart[item]
        sum += total
        items.append({'ebooks': ebooks, 'quantity': cart[item], 'total': total})
    request.session['sum'] = sum
    data = {'items': items}
    return render(request, 'Shop/basket.html', data)

@login_required(login_url='userAuthen')
def checkout(request):
    cart = request.session.get('cart')
    items = []
    sum = 0.00
    if cart:
        if not request.session.get('userId'):
            request.session['orderActive'] = True
            return redirect('userAuthen')
        cart = request.session.get('cart')
        date = datetime.datetime.now()
        # print("date:", date)
        customer = get_object_or_404(Customers, cid=request.session.get('userId'))
        order = Orders()
        order.odate = date.strftime('%Y-%m-%d %H:%M:%S')
        order.customer = customer
        for item in cart:
            # print(item, cart[item])
            ebooks = Ebook.objects.get(bid=item)
            total = ebooks.price * cart[item]
            sum += total
            items.append({'ebooks': ebooks, 'quantity': cart[item], 'total': total})
        request.session['sum'] = sum
        data = {'items': items, 'order': order}
        return render(request, 'Shop/checkout.html', data)
    else:
        messages.add_message(request, messages.WARNING, "No product in basket!!!..")
        return redirect('ebookShop')

@login_required(login_url='userAuthen')
def order(request):
    cart = request.session.get('cart')
    if cart is None:
        return redirect('ebookShop')
    items = []
    date = datetime.datetime.now()
    customer = get_object_or_404(Customers, cid=request.session.get('userId'))
    order = Orders()
    order.newOrderId()
    order.odate = date.strftime('%Y-%m-%d %H:%M:%S')
    order.customer = customer
    order.status = "1"
    order.save()
    for item in cart:  # get any key from cart
        ebooks = Ebook.objects.get(bid=item)
        quantity = cart[item]
        total = ebooks.price * cart[item]
        orderDetail = OrderDetails()
        orderDetail.order = order
        orderDetail.ebooks = ebooks
        orderDetail.oprice = ebooks.price
        orderDetail.quantity = quantity
        orderDetail.save()
        items.append({'ebooks': ebooks, 'quantity': cart[item], 'total': total})
    count = request.session.get('count')
    sum = request.session.get('sum')
    data = {'items': items, 'order': order, 'count': count, 'sum': sum}
    del request.session['cart']
    del request.session['count']
    del request.session['sum']
    return render(request, 'Shop/summary.html', data)

@login_required(login_url='userAuthen')
def clearBasket(request):
    del request.session['cart']
    del request.session['count']
    del request.session['sum']
    return redirect('ebookShop')

def showAllOrder(request):
    orders = []
    if request.session.get("userStatus") == 'customer':
        customer = get_object_or_404(Customers, cid=request.session.get('userId'))
        orders = None
        if customer:
            orders = Orders.objects.filter(customer=customer).order_by('odate').reverse()
        context = {'customer': customer, 'orders': orders}
        return render(request, 'Shop/showAllOrder.html', context)
    else: #employee
        orders = Orders.objects.filter(~Q(status='5')).exclude(status='6').exclude(status='7').order_by('odate').reverse() #อ่านใบสั่งซื้อที่ status 1-4
        context = {'orders': orders}
        return render(request, 'Shop/showAllOrder.html', context)

def showOrderDetail(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    if request.method == 'POST':
        return redirect('home')
    else:
        context = {'order': order}
        return render(request, 'Shop/showOrderDetail.html', context)

@login_required(login_url='userAuthen')
def showHistoryOrder(request):
    orders = []
    orders = Orders.objects.filter(Q(status='6') | Q(status='7') | Q(status='8'))
    context = {'orders': orders}
    return render(request, 'Shop/showHistoryOrder.html', context)

@login_required(login_url='userAuthen')
def orderConfirm(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employee, eid=request.session.get('userId'))
    confirm = Confirms()
    confirm.order = order
    confirm.employee = employee
    confirm.save()
    order.status = '2'
    order.save()
    return redirect('showAllOrder')

@login_required(login_url='userAuthen')
def moneyTransfer(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    form = TranfersForm(request.POST or None, files=request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '3'
            order.save()
        return redirect('showAllOrder')
    else:
        form = TranfersForm(initial={'order': order})
        form.setup()
        context = {'form': form, 'order': order}
        return render(request, 'Shop/moneyTransfer.html', context)

@login_required(login_url='userAuthen')
def moneyAccept(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employee, eid=request.session.get('userId'))
    accept = Accepts()
    accept.order = order
    accept.employee = employee
    accept.save()
    order.status = '4'
    order.save()
    return redirect('showAllOrder')

@login_required(login_url='userAuthen')
def bookSend(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employee, eid=request.session.get("userId"))
    form = SendForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '5'
            order.save()
        return redirect('showAllOrder')
    else:
        form = SendForm(initial={'order': order, 'employee': employee})
        context = {'form': form, 'order': order}
        return render(request, 'Shop/bookSend.html', context)

@login_required(login_url='userAuthen')
def orderCancel(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    form = CancelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '6'
            order.save()
        return redirect('showAllOrder')
    else:
        form = CancelForm(initial={'order': order})
        context = {'form': form, 'order': order}
        return render(request, 'Shop/orderCancel.html', context)

@login_required(login_url='userAuthen')
def orderReject(request, oid):
    order = get_object_or_404(Orders, oid=oid)
    employee = get_object_or_404(Employee, eid=request.session.get("userId"))
    form = RejectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            order.status = '7'
            order.save()
        return redirect('showAllOrder')
    else:
        form = RejectForm(initial={'order': order, 'employee': employee})
        context = {'form': form, 'order': order}
        return render(request, 'Shop/orderReject.html', context)

from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def pdfThaiReport(request):
    pdfmetrics.registerFont(TTFont('THSarabunNew', 'thsarabunnew-webfont.ttf'))
    template = get_template('pdfThaiReport.html')
    context = {"Name" : "อาจารย์พิชญะภาคย์  พิพิธพัฒน์ไพสิฐ"}
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("<h1><b>เกิดข้อผิดพลาด!!!</b> ไม่สามารถสร้างเอกสาร PDF ได้...</h2>", status=400)

def pdfProductReport(request):
    pdfmetrics.registerFont(TTFont('THSarabunNew', 'thsarabunnew-webfont.ttf'))
    template = get_template('pdfProductReport.html')
    ebook = Ebook.objects.all()
    context = {"ebook": ebook}
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("<h1><b>เกิดข้อผิดพลาด!!!</b> ไม่สามารถสร้างเอกสาร PDF ได้...</h2>", status=400)

import plotly.graph_objs as go

import pandas as pd
import plotly.express as px

def dashboardBarGraph(request):
    productsAll = Ebook.objects.all()
    products = []
    amounts = []
    for item in productsAll:
        products.append(item.name)
        amounts.append(item.getSaleAmount())
    # กรณีอ่านค่าจากบางฟิลด์ใน model มาใช้งาน
    # products = Products.objects.values_list('name', 'samplesale__amount')
    # df = pd.DataFrame(products,  columns=['Product', 'Amount'])
    df = pd.DataFrame({"Product":products, "Amount":amounts}, columns=['Product', 'Amount'])
    fig = px.bar(df, x='Product', y='Amount', title="แผนภูมิแท่งแสดงยอดขายแยกตามรายชื่อสินค้า")
    fig.update_layout(autosize = False, width = 600,  height = 400,
                      margin=dict(l=10, r=10, b=100, t=100, pad=5),
                      paper_bgcolor="aliceblue",)
    chart = fig.to_html()
    context = {'chart':chart}
    return render(request, "chart/dashboard.html", context)

def dashboardPieGraph(request):
    productsAll = Ebook.objects.all()
    products = []
    amounts = []
    for item in productsAll:
        products.append(item.name)
        amounts.append(item.getSaleAmount())
    df = pd.DataFrame({"Product": products, "Amount": amounts}, columns=['Product', 'Amount'])
    fig = px.pie(df, hole=.3, names='Product', values ='Amount', title="แผนภูมิวงกลมแสดงยอดขายแยกตามรายชื่อสินค้า")
    fig.update_layout(autosize=False, width=600, height=400,
                      margin = dict(l=10, r=10, b=100, t=100, pad=5 ),
                      paper_bgcolor = "aliceblue",)
    chart = fig.to_html()
    context = {'chart':chart}
    return render(request, 'chart/dashboard.html', context)

def dashboardLineChart(request):
    saleAll = Samplesale.objects.all().order_by('datesale')
    sales = {}
    for sale in saleAll:
        preiod = str(sale.datesale.month) + "-" + str(sale.datesale.year)
        if preiod in sales.keys():
            sales[preiod] += sale.amount
        else:
            sales[preiod] = sale.amount
    df = pd.DataFrame({"Month_Year":sales.keys(), "Amount":sales.values()}, columns=['Month_Year', 'Amount'])
    fig = px.line(df, x='Month_Year', y='Amount',  title='กราฟเส้นแสดงยอดขายแยกตามเดือน-ปี')
    fig.update_layout(autosize = False, width = 600,  height = 400,
                      margin = dict(l=10, r=10, b=100, t=100, pad=5),
                      paper_bgcolor = "aliceblue",)
    chart = fig.to_html()
    context = {'chart':chart}
    return render(request, "chart/dashboard.html", context)

def dashboardAreaChart(request):
    saleAll = Samplesale.objects.all().order_by('datesale')
    sales = {}
    for sale in saleAll:
        preiod = str(sale.datesale.month) + "-" + str(sale.datesale.year)
        if preiod in sales.keys():
            sales[preiod] += sale.amount
        else:
            sales[preiod] = sale.amount
    df = pd.DataFrame({"Month_Year": sales.keys(), "Amount": sales.values()}, columns=['Month_Year', 'Amount'])
    fig = px.area(df, x='Month_Year', y='Amount', title='กราฟพื้นที่แสดงยอดขายแยกตามเดือน-ปี')
    fig.update_layout(autosize=False, width=600, height=400,
                      margin = dict(l=10, r=10, b=100, t=100, pad=5),
                      paper_bgcolor = "aliceblue",)
    chart = fig.to_html()
    context = {'chart': chart}
    return render(request, "chart/dashboard.html", context)

# def dashboardAll(request):
#     productsAll = Ebook.objects.all()
#     products = []
#     amounts = []
#     productCount = len(productsAll)
#     totalSale=0.00
#     for item in productsAll:
#         products.append(item.name)
#         amounts.append(item.getSaleAmount())
#         totalSale += item.getSaleAmount()
#
#     df_product = pd.DataFrame({"Product": products, "Amount": amounts}, columns=['Product', 'Amount'])
#
#     fig_bar = px.bar(df_product, x='Product', y='Amount', title="แผนภูมิแท่งแสดงยอดขายแยกตามรายชื่อสินค้า")
#     fig_bar.update_layout(autosize=False, width=430, height=400,
#                           margin=dict(l=10, r=10, b=100, t=100, pad=5),
#                           paper_bgcolor="aliceblue", )
#     chart_bar = fig_bar.to_html()
#
#     fig_pie = px.pie(df_product, hole=.3, names='Product', values='Amount', title="แผนภูมิวงกลมแสดงยอดขายแยกตามรายชื่อสินค้า")
#     fig_pie.update_layout(autosize=False, width=430, height=400,
#                           margin=dict(l=10, r=10, b=100, t=100, pad=5),
#                           paper_bgcolor="aliceblue", )
#     chart_pie = fig_pie.to_html()
#
#     saleAll = Samplesale.objects.all().order_by('datesale')
#     sales = {}
#     for sale in saleAll:
#         preiod = str(sale.datesale.month) + "-" + str(sale.datesale.year)
#         if preiod in sales.keys():
#             sales[preiod] += sale.amount
#         else:
#             sales[preiod] = sale.amount
#     df_sale = pd.DataFrame({"Month_Year": sales.keys(), "Amount": sales.values()}, columns=['Month_Year', 'Amount'])
#
#     fig_line = px.line(df_sale, x='Month_Year', y='Amount', title='กราฟเส้นแสดงยอดขายแยกตามเดือน-ปี')
#     fig_line.update_layout(autosize=False, width=430, height=400,
#                            margin=dict(l=10, r=10, b=100, t=100, pad=5),
#                            paper_bgcolor="aliceblue", )
#     chart_line = fig_line.to_html()
#
#     fig_area = px.area(df_sale, x='Month_Year', y='Amount', title='กราฟพื้นที่แสดงยอดขายแยกตามเดือน-ปี')
#     fig_area.update_layout(autosize=False, width=430, height=400,
#                            margin=dict(l=10, r=10, b=100, t=100, pad=5),
#                            paper_bgcolor="aliceblue", )
#     chart_area = fig_area.to_html()
#     context = {'chart_bar': chart_bar, 'chart_pie': chart_pie,
#                'chart_line':chart_line, 'chart_area':chart_area,
#                "productCount":productCount, "totalSale":totalSale}
#     return render(request, 'dashboardMultiple.html', context)