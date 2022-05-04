from random import randrange
from django.shortcuts import redirect, render
from myapp.models import Book, Cart, Order, Sub_Item, User
from myapp.models import Item
from random import choices, randrange
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# Create your views here.

def index(request):
    return render(request,'index.html')

def sign_in(request):
    if request.method == 'POST':
        try:
            uid = User.objects.get(email=request.POST['email'])
            if request.POST['password'] == uid.password:
                request.session['email'] = request.POST['email']
                return redirect('index')
            return render(request,'sign-in.html',{'msg':'Pasword is incorrect'})
        except:
            return render(request,'sign-in.html',{'msg':'Acccount does not exists'})
    return render(request,'sign-in.html')




def sign_up(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = 'email are already exist'
        except:
            if request.POST['password'] == request.POST['cpassword']:
                otp = randrange(1000,9999)
                subject = 'otp verification'
                message = f'Your OTP is {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                global temp
                temp = {
                    'fname' : request.POST['fname'],
                    'lname' : request.POST['lname'],
                    'email' : request.POST['email'],
                    'mobile' : request.POST['mobile'],
                    'password' : request.POST['password'],
                }
                return render(request,'otp.html',{'msg':'OTP sent on your Email!!','otp':otp})
            return render(request,'sign-up.html',{'msg':'Both are not same'})
            
    return render(request,'sign-up.html')

def otp(request):
    if request.method == "POST":
        if request.POST['uotp'] == request.POST['otp']:
            global temp
            User.objects.create(
                fname = temp['fname'],
                lname = temp['lname'],
                email = temp['email'],
                mobile = temp['mobile'],
                password = temp['password'],
            )
            del temp
            return render(request,'sign-in.html',{'msg':'Account Created'})
        return render(request,'otp.html',{'msg':'Invalid OTP','otp':request.POST['otp']})
    return render(request,'sign-up.html')
    

def profile(request):
    return render(request,'profile.html')


def forgot_password(request):
    if request.method == 'POST':
        try:
            uid = User.objects.get(email=request.POST['email'])
            s = 'qweertyuiopasdfghklxcvbnm12345684556$%$#'
            password = ''.join(choices(s,k=8))  
            subject = 'Password Has Been Reset'
            message = f'Your New password is {password}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            uid.password = password
            uid.save()
            return render(request,'sign-in.html',{'msg':'Ne wpassword sent on your email'})

        except:
            return render(request,'forgot-password.html',{'msg':'Account does not exist'})
    return render(request,'forgot-password.html')

def header(request):
      return render(request,'header.html')

def logout(request):
     del request.session['email']
     return render(request,'sign-in.html')

def menu(request):
    all_item = Sub_Item.objects.all()
    return render(request,'menu.html',{'all_items':all_item})



def cart(request,pk):
    print('----------------------------------------')
    sub = Sub_Item.objects.get(id=pk)
    user = User.objects.get(email =request.session['email'])
    Cart.objects.create(
        user = user,
        food = sub
    )
    return redirect('menu')


def item(request):
    if request.method == "POST":
        try:
            
            obj= Item.objects.get(name=request.POST['pname'])
            msg = 'This is item already exists.'
            return render(request,'item.html',{'msg':msg})
        except:
            Item.objects.create(
            name = request.POST['pname'],
            )
            msg = 'success added.'
            return render(request,'item.html',{'msg':msg})
    else:
        return render(request,'item.html')


def sub_item(request):
    if request.method == "POST":
        try:
            sub = Sub_Item.objects.get(main_item=request.POST['main_item'])
            msg = 'This is item already exists.'
            return render(request,'sub_item',{'msg':msg})
        except:
            Sub_Item.objects.create(
                main_item = request.POST['main_item'],
                subitem_name = request.POST['subitem_name'],
                size = request.POST['size'],
                price = request.POST['price'],
            )    
            msg = 'success added.'
            return render(request,'sub-item.html',{'msg':msg})
    else:
        return render(request,'sub-item.html')


razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def Cart1(request):
    user = User.objects.get(email =request.session['email'])
    cart = Cart.objects.filter(user=user)
    am = 0
    book = Book.objects.create(
        user = user,  
    )
    for i in cart:
        am += i.food.price
        Order.objects.create(
            item = i.food,
            book = book
        )
    book.amount = am
    book.save()
    currency = 'INR'
    amount = am*100 # Rs. 200

    

	# Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = f'paymenthandler/{book.id}'

	# we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['cart'] = cart
    context['am'] = am
    return render(request,'Cart1.html',context=context)

def viewbook(request):
    user =  User.objects.get(email=request.session['email'])
    book = Order.objects.filter(book__verify=True, book__user=user)
    return render(request,'viewbook.html',{'uid':user,'book':book})

                

# authorize razorpay client with API Keys.

def homepage(request):
	currency = 'INR'
	amount = 20000 # Rs. 200

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	context = {}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['razorpay_amount'] = amount
	context['currency'] = currency
	context['callback_url'] = callback_url
    # context['cart'] = 
	return render(request, 'index.html', context=context)

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.

@csrf_exempt
def paymenthandler(request,pk):
 
    # only accept POST request.
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.session['email'])

            book = Book.objects.get(id=pk)
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            # if result is None:
            amount = book.amount*100  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                book.pay_id = payment_id
                book.verify = True
                book.save()
                cart = Cart.objects.filter(user=user)
                cart.delete()
                # render success page on successful caputre of payment
                return render(request, 'success.html',{'book':book})
            except:

                # if there is an error while capturing payment.
                return render(request, 'fail.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

def remove_item(request,pk):
    user = User.objects.get(email=request.session['email'])
    cart_item= Cart.objects.get(id=pk)
    cart_item.delete()
    return redirect('Cart1')

