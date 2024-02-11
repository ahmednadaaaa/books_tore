from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse 
from .models import *
from .forms import OrderForm,CreateNewUser,CustomerForm
from .filters import OrderFilter
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate ,login  , logout 
from django.contrib.auth.decorators import  login_required
from .decorators import notLoggedUsers , allowedUsers, forAdmins
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.utils import timezone

import requests
from django.conf import settings



@login_required(login_url='login')
#@allowedUsers(allowedGroups=['admin'])
@forAdmins
def home(request):
    
    customers = Customer.objects.all()
    orders = Order.objects.all()
  
    context = {'customers': customers ,
               'orders': orders,
                }
               
    return render(request , 'bookstore/dashboard.html',context)

 


def books(request): 
    books = Book.objects.all()
    name = request.GET.get('searchname')
    if name:
        books = books.filter(name__contains=name)
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    return render(request, 'bookstore/books.html', {'books': books })


@login_required(login_url='login')
#@forAdmins
def books_detail(request,pk): 
    books = get_object_or_404(Book, id=pk) 
    related_books = Book.objects.filter(category=books.category).exclude(id=books.id)

    context = {
        'books': books,
        'related_books': related_books,
    }
    return render(request , 'bookstore/book_detail.html',context)


@login_required(login_url='login')
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    number_orders = orders.count()

    searchFilter = OrderFilter(request.GET , queryset=orders)
    orders = searchFilter.qs


    context = {'customer': customer ,'myFilter': searchFilter ,
               'orders': orders,'number_orders': number_orders }
    return render(request , 'bookstore/customer.html',context)



# def create(request): 
#     form = OrderForm()
#     if request.method == 'POST':
#        # print(request.POST)
#        form = OrderForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('/')
#     context = {'form':form}

#     return render(request , 'bookstore/my_order_form.html', context )

@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def create(request,pk): 
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('book', 'status'),extra=8)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)
    # form = OrderForm()
    if request.method == 'POST':
       # print(request.POST)
      # form = OrderForm(request.POST)
      formset = OrderFormSet(request.POST , instance=customer)
      if formset.is_valid():
           formset.save()
           return redirect('/')
    #context = {'form':form}
    context = {'formset':formset}

    return render(request , 'bookstore/my_order_form.html', context )



@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def update(request,pk): 
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) 
    if request.method == 'POST': 
       form = OrderForm(request.POST, instance=order)
       if form.is_valid():
           form.save()
         
           return redirect('/')

    context = {'form':form}

    return render(request , 'bookstore/my_order_form.html', context )

@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def delete(request,pk): 
    order = Order.objects.get(id=pk) 
    if request.method == 'POST':  
        order.delete()
        return redirect('/')

    context = {'order':order}

    return render(request , 'bookstore/delete_form.html', context )




# def login(request):  
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:

#     context = {}

#     return render(request , 'bookstore/login.html', context )

@notLoggedUsers
def register(request):   
            form = CreateNewUser()
            if request.method == 'POST': 
                   form = CreateNewUser(request.POST)
                   if form.is_valid():

                       recaptcha_response = request.POST.get('g-recaptcha-response')
                       data = {
                           'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                           'response' : recaptcha_response
                       }
                       r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                       result = r.json()
                       if result['success']:
                           user = form.save()
                           username = form.cleaned_data.get('username')
                           messages.success(request , username + ' Created Successfully !')
                           return redirect('books')
                       else:
                          messages.error(request ,  ' invalid Recaptcha please try again!')  
 
        
            context = {'form':form}

            return render(request , 'bookstore/register.html', context )


@notLoggedUsers
def userLogin(request):  
  
        if request.method == 'POST': 
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request , username=username, password=password)
            if user is not None:
             login(request, user)
             return redirect('books')
            else:
                messages.info(request, 'Credentials error')
    
        context = {}

        return render(request , 'bookstore/login.html', context )


def userLogout(request):  
    logout(request)
    return redirect('login') 


@login_required(login_url='login')
@allowedUsers(allowedGroups=['customer'])
def userProfile(request):  
     
    orders = request.user.customer.order_set.all()

    t_orders = orders.count()
    p_orders = orders.filter(status='Pending').count()
    d_orders = orders.filter(status='Delivered').count()
    in_orders = orders.filter(status='in progress').count()
    out_orders = orders.filter(status='out of order').count()
    context = { 
               'orders': orders,
               't_orders': t_orders,
               'p_orders': p_orders,
               'd_orders': d_orders,
               'in_orders': in_orders,
               'out_orders': out_orders}

    
    return render(request , 'bookstore/profile.html', context )




@login_required(login_url='login')

def profileInfo(request):   
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST': 
         form = CustomerForm(request.POST , request.FILES, instance=customer)
         if form.is_valid():
             form.save()


    context = {'form':form}

    
    return render(request , 'bookstore/profile_info.html', context )


def add_to_cart(request):

    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous :

        pro_id = request.GET['pro_id']
        qty = request.GET['qty']

        order = Order.objects.all().filter(user=request.user, is_finished=False)

        if not Book.objects.all().filter(id=pro_id).exists():
            return redirect('books_detail')
        pro = Book.objects.get(id=pro_id)

        if order:
            messages.success(request,'يوجد طلب قديم')
            old_order = Order.objects.get(user=request.user.id, is_finished=False)
            if OrderDetail.objects.all().filter(order=old_order, product=pro).exists():
                orderdetails = OrderDetail.objects.get(order=old_order, product=pro)
                orderdetails.quantity += int(qty)
                orderdetails.save()
            else :
                orderdetails = OrderDetail.objects.create(product=pro,
                order=old_order, price=pro.price, quantity=qty)
            messages.success(request, 'was added to cart for old order')
        else :
            messages.success(request,'هنا سوف يتم عمل طلب')
            new_order = Order()
            new_order.user =request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            oderdetails = OrderDetail.objects.create(product=pro, order=new_order, price=pro.price, quantity=qty)
            messages.success(request, 'was added to cart for new order')

        return redirect('/books/' + request.GET['pro_id'])

    else:

      return redirect('books')




def cart(request):
    context = None
    if Order.objects.all().filter(user=request.user.id, is_finished=False):
        order = Order.objects.get(user=request.user.id, is_finished=False)
        orderdetails = OrderDetail.objects.all().filter(order=order)
        total = 0
        for sub in orderdetails:
            total +=sub.price * sub.quantity

        context = {
            'order':order,
            'orderdetails':orderdetails,
            'total':total,

        }

    return render(request, 'bookstore/cart.html', context)


def remove_from_cart(request, orderdetails_id):
   if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    orderdetails = OrderDetail.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id==request.user.id:
     orderdetails.delete()
    return redirect('cart')


def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetail.objects.get(id=orderdetails_id)
        orderdetails.quantity +=1
        orderdetails.save()

    return redirect('cart')


def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetail.objects.get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            orderdetails.quantity -= 1
            orderdetails.save()

    return redirect('cart')


def show_orders(request):
    context = None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user)
        if all_orders:
            for x in all_orders:
                order = Order.objects.get(id=x.id)
                orderdetails = OrderDetail.objects.all().filter(order=order)
                total = 0
                for sub in orderdetails:
                    total +=sub.price * sub.quantity
                    x.total = total
                    x.items_count = orderdetails.count
    context = {'all_orders':all_orders}
    return render(request, 'order/show_orders.html', context)



def payment(request):
    context = None
    ship_address = None
    ship_phone =None
    card_number = None
    expire = None
    security_code = None
    is_added = None
    if request.method == 'POST' and 'btnpayment' in request.POST and \
            'ship_address' in request.POST and 'ship_phone' in request.POST and \
             'expire' in request.POST and  'card_number' in request.POST:
              #هنا عملية الدفع بعد الضغط علي الزر

              ship_address = request.POST['ship_address']
              ship_phone =  request.POST['ship_phone']
              card_number =  request.POST['card_number']
              expire =  request.POST['expire']
              security_code =  request.POST['security_code']
              if request.user.is_authenticated and not request.user.is_anonymous:
                    if Order.objects.all().filter(user=request.user.id, is_finished=False):
                        order = Order.objects.get(user=request.user.id, is_finished=False)
                        payment = Payment(order=order, shipment_address=ship_address,
                                          shipment_phone=ship_phone, card_number=card_number, expire=expire,
                                          security_code=security_code)
                        payment.save()
                        order.is_finished = True
                        order.save()
                        is_added = True
                        messages.success(request, 'your order is finished')
              context = {
                            'ship_address': ship_address,
                            'ship_phone': ship_phone,
                            'card_number': card_number,
                            'expire': expire,
                            'security_code': security_code,
                            'is_added': is_added,
                  }


    else:

        if Order.objects.all().filter(user=request.user.id, is_finished=False):
            order = Order.objects.get(user=request.user.id, is_finished=False)
            orderdetails = OrderDetail.objects.all().filter(order=order)
            total = 0
            for sub in orderdetails:
                total +=sub.price * sub.quantity

            context = {
                'order':order,
                'orderdetails':orderdetails,
                'total':total,

            }
    return render(request , 'bookstore/payment.html')#{'books': books }