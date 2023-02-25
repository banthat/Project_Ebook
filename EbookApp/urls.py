from django.urls import path
from EbookApp import views

urlpatterns = [
    path('', views.home, name='home'),

    path('categoryList', views.categoryList, name='categoryList'),
    path('categoryNew', views.categoryNew, name='categoryNew'),
    path('<id>/categoryUpdate', views.categoryUpdate, name='categoryUpdate'),
    path('<id>/categoryDelete', views.categoryDelete, name='categoryDelete'),

    path('writerList', views.writerList, name='writerList'),
    path('writerNew', views.writerNew, name='writerNew'),
    path('<wid>/writerUpdate', views.writerUpdate, name='writerUpdate'),
    path('<wid>/writerDelete', views.writerDelete, name='writerDelete'),

    path('ebookList', views.ebookList, name='ebookList'),
    path('ebookNew', views.ebookNew, name='ebookNew'),
    path('<bid>/ebookUpdate', views.ebookUpdate, name='ebookUpdate'),
    path('<bid>/ebookDelete', views.ebookDelete, name='ebookDelete'),

    path('employeeList', views.employeeList, name='employeeList'),
    path('employeeNew', views.employeeNew, name='employeeNew'),
    path('<eid>/employeeUpdate', views.employeeUpdate, name='employeeUpdate'),
    path('<eid>/employeeDelete', views.employeeDelete, name='employeeDelete'),

    path('customerList', views.customerList, name='customerList'),
    path('customerRegister', views.customerRegister, name='customerRegister'),
    path('<cid>/customerUpdate', views.customerUpdate, name='customerUpdate'),

    path('userAuthen', views.userAuthen, name='userAuthen'),
    path('userLogout', views.userLogout, name='userLogout'),
    path('userChangePassword', views.userChangePassword, name='userChangePassword'),
    path('<userId>/userResetPassword', views.userResetPassword, name='userResetPassword'),

    path('ebookShop', views.ebookShop, name='ebookShop'),
    path('ebook_1', views.ebook_1, name='ebook_1'),
    path('ebook_2', views.ebook_2, name='ebook_2'),
    path('ebook_3', views.ebook_3, name='ebook_3'),
    path('basket', views.basket, name='basket'),
    path('checkout', views.checkout, name='checkout'),
    path('order', views.order, name='order'),
    path('clearBasket', views.clearBasket, name='clearBasket'),

    path('showAllOrder', views.showAllOrder, name='showAllOrder'),
    path('showHistoryOrder', views.showHistoryOrder, name='showHistoryOrder'),
    path('<oid>/showOrderDetail', views.showOrderDetail, name='showOrderDetail'),
    path('<oid>/orderConfirm', views.orderConfirm, name='orderConfirm'),
    path('<oid>/moneyTransfer', views.moneyTransfer, name='moneyTransfer'),
    path('<oid>/moneyAccept', views.moneyAccept, name='moneyAccept'),
    path('<oid>/bookSend', views.bookSend, name='bookSend'),
    path('<oid>/orderCancel', views.orderCancel, name='orderCancel'),
    path('<oid>/orderReject', views.orderReject, name='orderReject'),

    path('pdfThaiReport', views.pdfThaiReport, name='pdfThaiReport'),
    path('pdfProductReport', views.pdfProductReport, name='pdfProductReport'),

    path('dashboardBarGraph', views.dashboardBarGraph, name='dashboardBarGraph'),
    path('dashboardPieGraph', views.dashboardPieGraph, name='dashboardPieGraph'),
    path('dashboardLineChart', views.dashboardLineChart, name='dashboardLineChart'),
    path('dashboardAreaChart', views.dashboardAreaChart, name='dashboardAreaChart'),
    # path('dashboardAll', views.dashboardAll, name='dashboardAll'),

]
