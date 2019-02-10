from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from website.forms import *
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from website.models import *

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
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return HttpResponseRedirect('/')

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")


    return render(request, 'login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/')


def product_sell(request):
    if request.method == 'GET':
        product_form = ProductForm()
        template_name = 'product/product_sell.html'
        return render(request, template_name, {'product_form': product_form})

    elif request.method == 'POST':
        form_data = request.POST

        p = Product(
            seller = request.user,
            title = form_data['title'],
            description = form_data['description'],
            price = form_data['price'],
            quantity = form_data['quantity'],
        )
        p.save()
        template_name = 'product/success.html'
        return render(request, template_name, {})

def product_cat(request):
    product_cats = ProductType.objects.all()
    template_name = 'product/product_cat.html'
    return render(request, template_name, {'categories': product_cats})

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
    return render(request, template_name, {'product': product})

# ===================================================
# My Account Begin
# ===================================================

def my_account(request, user_id):
    '''user account page'''

    template_name = 'my_account/my_account.html'
    user = User.objects.get(id=user_id)
    sql = '''SELECT id, name, substr(accountNum, -4, 4) as four
            FROM website_paymenttype 
             WHERE buyer_id = %s'''
    payments = PaymentType.objects.raw(sql, [user_id])
    context = {
        'user': user,
        'payments': payments,
    }
    print('user', user_id)
    print('payments', payments)
   
    return render(request, template_name, context)

@login_required
def my_account_payment(request, user_id):
    '''add payment type for user'''
    template_name = 'my_account/my_account_payment.html'
    user = User.objects.get(id=user_id)

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
            new_payment_type = cursor.execute("INSERT INTO website_paymenttype VALUES (%s, %s, %s, %s, %s)", [None, req["name"], req["accountNum"], None, user_id])

        return HttpResponseRedirect(reverse('website:my_account', args=(user_id,)))

    return render(request, template_name, {'user': user, 'form':form.as_p()})
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

# ===================================================
# My Account End
# ===================================================






