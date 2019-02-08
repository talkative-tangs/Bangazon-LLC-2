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
    # my_account needs <int:user_id>/ added to path upon template setup
    path('my_account/', views.my_account, name='my_account')

    # order
    # product_detail/<int:product_id>/
    # order_payment
    # order_success
    # search_results
    # my_account_payment
    # my_account_order_history
    # my_account_order_detail - my_account/order_detail<int:product_id>/
]