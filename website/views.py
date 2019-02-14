from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from website.forms import *
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from website.models import *
from datetime import datetime

# Import this to use the direct db connection
from django.db import connection


#ORM WAY
# def index(request):
#     all_products = Product.objects.all()
#     template_name = 'index.html'
#     return render(request, template_name, {'products': all_products})
    # previous index
    # template_name = 'index.html'
    # return render(request, template_name, {})

def index(request):
    try:
        recent_products = Product.objects.raw('SELECT id, title FROM website_product ORDER BY id DESC LIMIT 20;')
    except Product.DoesNotExist:
        raise Http404("Products do not exist")

    template_name = 'index.html'
    return render(request, template_name, {'recent_products': recent_products})



# Create your views here.
def register(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        template_name = 'register.html'
        return render(request, template_name, {'user_form': user_form})


def login_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = {'next': request.GET.get('next', '/')}
    print("CONTEXT:", context)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            if request.POST.get('next') == '/':
              return HttpResponseRedirect('/')
            else:
              print("ELSE STATEMENT:", request.POST.get('next', '/'))
              return HttpResponseRedirect(request.POST.get('next', '/'))

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")


    return render(request, 'login.html', context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/')

@login_required
def product_sell(request):
    if request.method == 'GET':
        product_form = ProductForm()
        template_name = 'product/product_sell.html'
        return render(request, template_name, {'product_form': product_form})

    elif request.method == 'POST':
        form_data = request.POST
        product_form = ProductForm(form_data)

        if product_form.is_valid():
            seller = request.user.customer.id
            title = form_data['title']
            description = form_data['description']
            price = form_data['price']
            quantity = form_data['quantity']
            productType = form_data['productType']

            data = [seller, title, description, price, quantity, productType]

            with connection.cursor() as cursor:
                cursor.execute(f'''INSERT into website_product(
                    seller_id,
                    title,
                    description,
                    price,
                    quantity,
                    productType_id
                ) VALUES(%s, %s, %s, %s, %s, %s)''', data)
                product_id = cursor.lastrowid
                #
                return HttpResponseRedirect(reverse('website:product_detail', args=(product_id,)))
        else:
            raise ValidationError(_('Invalid value: %s'))


# def product_cat(request):
#     # product_cats = ProductType.objects.all()
#   try:
#     # By default, Django figures out a database table name by joining the model’s “app label” – the name you used in manage.py startapp – to the model’s class name, with an underscore between them.
#     categories = ProductType.objects.raw('SELECT * FROM website_producttype')
#     products = Product.objects.raw('SELECT * FROM website_product')
#   except ProductType.DoesNotExist:
#     raise Http404("Categories do not exist")

#   context = {'categories': categories, 'products': products}
#   template_name = 'product/product_cat.html'
#   return render(request, template_name, context)

def product_cat(request):
    electronics = ProductType.objects.raw('''
    SELECT website_producttype.name, website_product.title, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Electronics"
    ORDER BY website_product.id DESC LIMIT 3''')

    electronics_total = ProductType.objects.raw('''
    SELECT COUNT(website_product.id) as total_electronics, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Electronics"''')[0]

    computers = ProductType.objects.raw('''
    SELECT website_producttype.name, website_product.title, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Computers"
    ORDER BY website_product.id DESC LIMIT 3''')

    computers_total = ProductType.objects.raw('''
    SELECT COUNT(website_product.id) as total_computers, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Computers"''')[0]

    furniture = ProductType.objects.raw('''
    SELECT website_producttype.name, website_product.title, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Furniture"
    ORDER BY website_product.id DESC LIMIT 3''')

    furniture_total = ProductType.objects.raw('''
    SELECT COUNT(website_product.id) as total_furniture, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Furniture"''')[0]

    cars = ProductType.objects.raw('''
    SELECT website_producttype.name, website_product.title, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Cars"
    ORDER BY website_product.id DESC LIMIT 3''')

    cars_total = ProductType.objects.raw('''
    SELECT COUNT(website_product.id) as total_cars, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Cars"''')[0]

    misc = ProductType.objects.raw('''
    SELECT website_producttype.name, website_product.title, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Misc"
    ORDER BY website_product.id DESC LIMIT 3''')

    misc_total = ProductType.objects.raw('''
    SELECT COUNT(website_product.id) as total_misc, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Misc"''')[0]

    jewelry = ProductType.objects.raw('''
    SELECT website_producttype.name, website_product.title, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Jewelry"
    ORDER BY website_product.id DESC LIMIT 3''')

    jewelry_total = ProductType.objects.raw('''
    SELECT COUNT(website_product.id) as total_jewelry, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Jewelry"''')[0]

    books = ProductType.objects.raw('''
    SELECT website_producttype.name, website_product.title, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Books"
    ORDER BY website_product.id DESC LIMIT 3''')

    books_total = ProductType.objects.raw('''
    SELECT COUNT(website_product.id) as total_books, website_product.id
    FROM website_product
    JOIN website_producttype ON website_product.productType_id = website_producttype.id
    WHERE website_producttype.name = "Books"''')[0]

    context = {'electronics': electronics, 'computers': computers, 'jewelry': jewelry, 'books': books, 'misc': misc, 'cars': cars, 'furniture': furniture,
    'computers_total': computers_total, 'books_total': books_total, 'jewelry_total': jewelry_total, 'misc_total': misc_total, 'electronics_total': electronics_total, 'cars_total': cars_total, 'furniture_total': furniture_total}
    template_name = 'product/product_cat.html'
    return render(request, template_name, context)


#ORM WAY
# def product_detail(request, product_id):
#     product = Product.objects.get(id=product_id)
#     template_name = 'product/product_detail.html'
#     return render(request, template_name, {'product': product})

def product_detail(request, product_id):
    try:
        sql = '''SELECT id, seller_id FROM website_product WHERE id = %s'''
        product = Product.objects.raw(sql, [product_id])[0]
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    template_name = 'product/product_detail.html'
    return render(request, template_name, {'product': product })

# ===================================================
# My Account Begin
# ===================================================

def my_account(request, user_id):
    '''user account page'''
    currentuser = request.user
    template_name = 'my_account/my_account.html'
    user = User.objects.get(id=user_id)
    context = {
        # 'user': user,
        'currentuser': currentuser.customer.id,
    }

    return render(request, template_name, context)

@login_required
def my_account_payment(request, user_id):
    '''user account page with payment details'''

    currentuser = request.user
    template_name = 'my_account/my_account_payment.html'
    user = User.objects.get(id=user_id)
    sql = '''SELECT id, name, buyer_id, substr(accountNum, -4, 4) as four
            FROM website_paymenttype
             WHERE buyer_id = %s and deletedDate isnull'''
    payments = PaymentType.objects.raw(sql, [currentuser.customer.id])
    context = {
        'user': user,
        'payments': payments,
    }

    return render(request, template_name, context)

@login_required
def my_account_payment_add(request, user_id):
    '''add payment type for user'''
    template_name = 'my_account/my_account_payment_add.html'
    user = User.objects.get(id=user_id)
    currentuser = request.user


    if request.method == "GET":
            #No data submitted, create a blank form
            form = PaymentForm()

    if request.method == "POST":
        req = request.POST
        with connection.cursor() as cursor:
            payment_type_check = PaymentType.objects.raw("SELECT * FROM website_paymenttype WHERE name=%s AND accountNum=%s", [req["name"], req["accountNum"]])
            if payment_type_check:
                error = True
                return render(request, template_name, {'error':error})
            new_payment_type = cursor.execute("INSERT INTO website_paymenttype VALUES (%s, %s, %s, %s, %s)", [None, req["name"], req["accountNum"], None, currentuser.customer.id])

        return HttpResponseRedirect(reverse('website:my_account_payment', args=(user_id,)))

    return render(request, template_name, {'user': user, 'form':form.as_p()})

@login_required
def my_account_order_history(request, user_id):
    '''view order history of current user'''
    buyer_id = request.user
    try:
        sql = '''SELECT * FROM website_order WHERE buyer_id = %s and paymentType_id IS NOT NULL'''
        orders = Order.objects.raw(sql, [buyer_id.customer.id])
    except Order.DoesNotExist:
        raise Http404("No orders exist")

    template_name = 'my_account/my_account_order_history.html'

    return render(request, template_name, {'orders': orders})

@login_required
def my_account_order_detail(request, order_id):
    '''view order detail of selected order'''

    order_id = order_id

    try:
        sql = '''SELECT *
                FROM website_order as wo
                LEFT JOIN website_productorder as wpo ON wo.id = wpo.order_id
                LEFT JOIN website_product as wp ON wpo.product_id = wp.id
                WHERE order_id = %s'''
        products = Order.objects.raw(sql, [order_id])
        totalsql = '''SELECT wo.id, SUM(price) as order_total
                FROM website_order as wo
                LEFT JOIN website_productorder as wpo ON wo.id = wpo.order_id
                LEFT JOIN website_product as wp ON wpo.product_id = wp.id
                WHERE order_id = %s'''
        ordertotal = Order.objects.raw(totalsql, [order_id])[0]
    except Order.DoesNotExist:
        raise Http404("No orders exist")

    template_name = 'my_account/my_account_order_detail.html'

    return render(request, template_name, {'order_id': order_id, 'products': products, 'ordertotal': ordertotal})

# ------------------------------------
# ORM WAY
# ------------------------------------
# @login_required
# def my_account_payment(request, user_id):
#     '''Add a new payment method for a particular user'''

#     print('user id', user_id)
#     template_name = 'my_account/my_account_payment.html'
#     user = User.objects.get(id=user_id)
#     print('user', user.id)

#     if request.method != 'POST':
#         #No data submitted, create a blank form
#         form = PaymentForm()
#     else:
#         #POST data submitted; process data
#         form = PaymentForm(data=request.POST)
#         # if form.is_valid():
#         name = request.POST['name']
#         accountNum = request.POST['accountNum']
#         new_payment = PaymentType(
#             name=name,
#             accountNum=accountNum,
#             buyer_id=user.id
#         )
#         new_payment.save()

#         return HttpResponseRedirect(reverse('website:my_account', args=(user_id,)))

@login_required
def my_account_payment_delete(request, payment_type_id):
    '''delete payment method from payment method list'''
    currentuser = request.user
    if request.method == 'POST':
        with connection.cursor() as cursor:
            selected_payment = payment_type_id
            now = str(datetime.now())

            cursor.execute("UPDATE website_paymenttype SET deletedDate = %s WHERE id = %s", [now, selected_payment])
            sql = '''SELECT id, buyer_id FROM website_paymenttype WHERE id = %s'''
            user = PaymentType.objects.raw(sql, [payment_type_id])[0]

        return HttpResponseRedirect(reverse('website:my_account_payment', args=(currentuser.customer.id,)))


# ===================================================
# My Account End
# ===================================================

@login_required
def search_results(request):

    template_name = 'search/search_results.html'

    query = request.GET.get('q', '')
    if query:
        # query example
        results = Product.objects.filter(title__icontains=query).distinct()
    else:
        results = []
    return render(request, template_name, {'results': results, 'query': query})


# ===================================================
# Order Begin
# ===================================================

@login_required
def order_product(request, product_id):
    ''' first checks if user has any open orders '''
    # once logged in, query orders by user
    currentuser = request.user
    sql = '''SELECT *
          FROM website_order
          WHERE buyer_id = %s
          AND paymentType_id IS NULL'''

    try:
        open_order = Order.objects.raw(sql, [currentuser.customer.id])[0]
    except IndexError:
        open_order = None

    ''' if user has open order, grab order number and create new join relationship with order_id and product_id '''
    if open_order is not None:
      with connection.cursor() as cursor:
          cursor.execute("INSERT into website_productorder VALUES (%s, %s, %s)", [ None, open_order.id, product_id ])
          return HttpResponseRedirect(reverse('website:order_detail', args=(open_order,)))

    else:
      with connection.cursor() as cursor:
          cursor.execute("INSERT into website_order VALUES (%s, %s, %s, %s)", [ None, None, currentuser.customer.id, None ])
          sql = ''' SELECT * FROM website_order ORDER BY id DESC LIMIT 1'''
          new_order = Order.objects.raw(sql,)[0]

          cursor.execute("INSERT into website_productorder VALUES (%s, %s, %s)", [ None, new_order.id, product_id])
          return HttpResponseRedirect(reverse('website:order_detail', args=(new_order.id,)))

@login_required
def shopping_cart(request):
    ''' first checks if user has any open orders '''
    # once logged in, query orders by user
    currentuser = request.user
    sql = '''SELECT *
          FROM website_order
          WHERE buyer_id = %s
          AND paymentType_id IS NULL'''

    try:
        open_order = Order.objects.raw(sql, [currentuser.customer.id])[0]
    except IndexError:
        open_order = None

    if open_order is not None:
        return HttpResponseRedirect(reverse('website:order_detail', args=(open_order,)))

    else:
        sql = ''' SELECT * FROM website_order ORDER BY id DESC LIMIT 1'''
        new_order = Order.objects.raw(sql,)[0]
        template_name = 'order/shopping_cart.html'
        return render(request, template_name)

def order_detail(request, order_id):
    '''order detail acts like a shopping cart for the user'''

    user = request.user
    sql = '''SELECT *
      FROM website_productorder
      WHERE order_id = %s'''

    orders = ProductOrder.objects.raw(sql, [order_id])

    template_name = 'order/order_detail.html'
    context = {'user': user, 'orders': orders, 'current_order_id': order_id}
    return render(request, template_name, context)


def order_cancel(request, order_id):
    ''' allows user to cancel order - product orders deleted from join table first before deleting order'''

    template_name = 'order/order_cancel_msg.html'
    if request.method == 'POST':
      with connection.cursor() as cursor:

          cursor.execute("DELETE FROM website_productorder WHERE order_id = %s", [order_id])
          cursor.execute("DELETE FROM website_order WHERE id = %s", [order_id])

    return render(request, template_name)


def order_product_to_delete(request, order_product_to_delete):
    ''' allows user to delete product from order '''

    sql='''SELECT * FROM website_productorder p
    WHERE p.id = %s
    '''
    product_order_id = ProductOrder.objects.raw(sql, [order_product_to_delete])[0]
    print("PRODUCT ORDER ID:", product_order_id)
    print("ORDER ID:", product_order_id.order_id)

    if request.method == 'POST':
      with connection.cursor() as cursor:
          cursor.execute("DELETE FROM website_productorder WHERE id = %s", [order_product_to_delete])

    return HttpResponseRedirect(reverse('website:order_detail', args=(product_order_id.order_id,)))


def order_payment(request, order_id):
    '''adds payment type and completes order'''

    currentuser = request.user
    sql = '''SELECT *
      FROM website_productorder
      WHERE order_id = %s'''
    orders = ProductOrder.objects.raw(sql, [order_id])

    user_payments_sql = '''SELECT website_paymenttype.id, website_paymenttype.name
        FROM website_paymenttype
        JOIN website_customer ON website_paymenttype.buyer_id = website_customer.id
        WHERE website_paymenttype.buyer_id = %s AND website_paymenttype.deletedDate IS NULL'''

    payment_types = PaymentType.objects.raw(user_payments_sql, [currentuser.customer.id])

    template_name = 'order/order_payment.html'
    context = {'currentuser': currentuser, 'orders': orders, 'payment_types': payment_types, 'order_id': order_id }
    return render(request, template_name, context)


def order_success(request, order_id):
      '''adds payment type to order and redirects after successful order completion '''
      payment_id = request.POST["payment_type"]
      with connection.cursor() as cursor:
          cursor.execute("UPDATE website_order SET paymentType_id = %s WHERE website_order.id = %s", [payment_id, order_id])

      template_name = 'order/order_success.html'
      return render (request, template_name)

def product_books(request):
    books = Product.objects.filter(productType_id=4)
    template_name = 'product/product_books.html'
    return render(request, template_name, {'books': books})

def product_cars(request):
    cars = Product.objects.filter(productType_id=3)
    template_name = 'product/product_cars.html'
    return render(request, template_name, {'cars': cars})

def product_misc(request):
    misc = Product.objects.filter(productType_id=7)
    template_name = 'product/product_misc.html'
    return render(request, template_name, {'misc': misc})

def product_jewelry(request):
    jewelry = Product.objects.filter(productType_id=6)
    template_name = 'product/product_jewelry.html'
    return render(request, template_name, {'jewelry': jewelry})

def product_electronics(request):
    electronics = Product.objects.filter(productType_id=1)
    template_name = 'product/product_electronics.html'
    return render(request, template_name, {'electronics': electronics})

def product_furniture(request):
    furniture = Product.objects.filter(productType_id=2)
    template_name = 'product/product_furniture.html'
    return render(request, template_name, {'furniture': furniture})

def product_computers(request):
    computers = Product.objects.filter(productType_id=5)
    template_name = 'product/product_computers.html'
    return render(request, template_name, {'computers': computers})