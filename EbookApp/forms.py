from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'type')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',  'size': 50, 'maxlength': 50}),
            'type': forms.TextInput(attrs={'class': 'form-control',  'size': 50, 'maxlength': 50}),
        }
        labels = {
            'name': 'หมวดหมู่',
            'type': 'ประเภท',
        }

    def updateForm(self):
        self.fields['id'].widget.attrs['readonly'] = True
        self.fields['id'].label = 'รหัสหมวดหมู่ [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['type'].widget.attrs['readonly'] = True

class WriterForm(forms.ModelForm):
    class Meta:
        model = Writer
        fields = ('wid', 'name', 'publisher')
        widgets = {
            'wid': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'wid': 'รหัสนักเขียน',
            'name': 'ชื่อนักเขียน',
            'publisher': 'สำนักพิมพ์',
        }

    def updateForm(self):
        self.fields['wid'].widget.attrs['readonly'] = True
        self.fields['wid'].label = 'รหัสสินค้า [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['wid'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['publisher'].widget.attrs['readonly'] = True

class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ('bid', 'name', 'price', 'sellDate', 'picture', 'net' ,'desc', 'category', 'writer')
        widgets = {
            'bid': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'Min': 1}),
            'sellDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'ebook/*'}),
            'net': forms.NumberInput(attrs={'class': 'form-control', 'Min': 0}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'writer': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'bid': 'รหัสหนังสือ',
            'name': 'ชื่อหนังสือ',
            'price': 'ราคา',
            'sellDate': 'วันที่วางขาย',
            'picture': 'รูปภาพ',
            'net': 'จำนวน',
            'desc': 'รายละเอียด',
            'category': 'หมวดหมู่',
            'writer': 'นักเขียน'
        }

    def updateForm(self):
        self.fields['bid'].widget.attrs['readonly'] = True
        self.fields['bid'].label = 'รหัสสินค้า [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['bid'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['sellDate'].widget.attrs['readonly'] = True
        self.fields['picture'].widget.attrs['readonly'] = True
        self.fields['net'].widget.attrs['readonly'] = True
        self.fields['desc'].widget.attrs['readonly'] = True
        self.fields['category'].widget.attrs['readonly'] = True
        self.fields['writer'].widget.attrs['readonly'] = True

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('eid', 'name', 'position', 'telephone', 'password')

        STATUS_CHOICES = (
            ("Manager", "Manager"),
            ("Employee", "Employee"),
            ("Store", "Store"),
        )

        widgets = {
            'eid': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(choices=STATUS_CHOICES, attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'size': 55,'maxlength': 50}),
        }
        labels = {
            'eid': 'รหัสพนักงาน',
            'name': 'ชื่อ-สกุล',
            'position': 'ตำแหน่ง',
            'telephone': 'เบอร์โทร',
        }

    def updateForm(self):
        self.fields['eid'].widget.attrs['readonly'] = True
        self.fields['eid'].label = 'รหัสพนักงาน [ไม่อนุญาตให้แก้ไขได้]'
        self.fields['password'].widget = forms.HiddenInput()

    def deleteForm(self):
        self.fields['eid'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['position'].widget.attrs['readonly'] = True
        self.fields['telephone'].widget.attrs['readonly'] = True
        self.fields['password'].widget.attrs['readonly'] = True

class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('cid', 'name', 'telephone', 'password')

        widgets = {
            'cid': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
        }
        labels = {
            'cid': 'รหัสลูกค้า',
            'name': 'ชื่่อ',
            'telephone': 'เบอร์โทร',
            'address': 'ที่อยู่',
            'password': 'รหัสผ่าน',
        }

    def updateForm(self):
        self.fields['cid'].widget.attrs['readonly'] = True
        self.fields['cid'].label = 'รหัสลูกค้า [ไม่อนุญาตให้แก้ไขได้]'
        self.fields['password'].widget = forms.HiddenInput()

class ChangePasswordForm(forms.Form):
    userId = forms.CharField(label='รหัสประจำตัวผู้ใช้', max_length=50,
                             widget=forms.TextInput(attrs={'class':'form-control', 'readonly': True}))
    oldPassword = forms.CharField(label='รหัสผ่านเดิม', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    newPassword = forms.CharField(label='รหัสผ่านใหม่', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirmPassword = forms.CharField(label='ยืนยันรหัสผ่านใหม่',  max_length=100,
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ResetPasswordForm(forms.Form):
    userId = forms.CharField(label='รหัสประจำตัวผู้ใช้', max_length=50,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':True}))
    newPassword = forms.CharField(label='รหัสผ่านใหม่', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirmPassword = forms.CharField(label='ยืนยันรหัสผ่านใหม่',  max_length=100,
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class TranfersForm(forms.ModelForm):
    class Meta:
        model = Transfers
        fields = ('order', 'reference', 'bank', 'bill', 'comment')
        widgets = {
            'order': forms.HiddenInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'size': 40, 'maxlength': 35}),
            'bank': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'bill': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'order': 'ใบสั่งซื้อสินค้า',
            'reference': 'หมายเลขใบโอนเงิน',
            'bank': 'จากธนาคาร',
            'bill': 'ไฟล์สลิปใบโอน',
            'comment': 'หมายเหตุ ',
        }
    def setup(self):
        self.fields['comment'].required = False


class SendForm(forms.ModelForm):
    class Meta:
        model = Send
        fields = ('order', 'employee', 'company', 'tag', 'comment')
        widgets = {
            'order': forms.HiddenInput(attrs={'class': 'form-control'}),
            'employee': forms.HiddenInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'tag': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'order': 'ใบสั่งซื้อสินค้า',
            'employee': 'พนักงาน',
            'company': 'บริษัทขนส่ง',
            'tag': 'หมายเลขพัสดุ',
            'comment': 'หมายเหตุ',
        }

class CancelForm(forms.ModelForm):
    class Meta:
        model = Cancel
        fields = ('order', 'reason')
        widgets = {
            'order': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'order': 'ใบสั่งซื้อสินค้า',
            'reason': 'เหตุผลในการยกเลิกใบสั่งซื้อ',
        }

class RejectForm(forms.ModelForm):
    class Meta:
        model = Reject
        fields = ('order', 'employee', 'reason')
        widgets = {
            'order': forms.HiddenInput(attrs={'class': 'form-control'}),
            'employee': forms.HiddenInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'order': 'ใบสั่งซื้อสินค้า',
            'employee': 'พนักงาน',
            'reason': 'เหตุผลในการปฏิเสธการสั่งซื้อ',
        }
