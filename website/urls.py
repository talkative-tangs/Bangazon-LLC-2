from django.urls import path

from . import views

app_name = "website"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('product_sell/', views.product_sell, name='product_sell'),
    path('product_cat/', views.product_cat, name='product_cat'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('my_account/<int:user_id>/', views.my_account, name='my_account'),
    path('my_account/payment/<int:user_id>/', views.my_account_payment, name='my_account_payment'),
    path('my_account/payment/add/<int:user_id>/', views.my_account_payment_add, name='my_account_payment_add'),
    path('my_account/payment/delete/<int:payment_type_id>',views.my_account_payment_delete, name='my_account_payment_delete'),
    path('search_results/', views.search_results, name='search_results'),

   
   

    # order
    # product_detail/<int:product_id>/
    # order_payment
    # order_success
    # search_results
    # my_account_payment
    # my_account_order_history
    # my_account_order_detail - my_account/order_detail<int:product_id>/
]