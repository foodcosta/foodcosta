from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from random import choices, randrange
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def index(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'index.html')
    except:
        return render(request,'sign-in.html',{'msg':'Session has expired'})

def sign_in(request):
    if request.method == 'POST':
        try:
            uid = User.objects.get(email=request.POST['email'])
            if request.POST['password'] == uid.password:
                request.session['email'] = request.POST['email']
                return render(request,'index.html',{'uid':uid})
            return render(request,'sign-in.html',{'msg':'Pasword is incorrect'})
        except:
            return render(request,'sign-in.html',{'msg':'Acccount does not exists'})
    return render(request,'sign-in.html')

def sign_up(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = 'Email already exist'
            return render(request,'sign-up.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                otp = randrange(1000,9999)
                subject = 'OTP verification'
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

def logout(request):
    del request.session['email']
    return render(request,'sign-in.html')


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
            return render(request,'forgot-password.html',{'msg':'Ne wpassword sent on your email'})

        except:
            return render(request,'forgot-password.html',{'msg':'Account does not exist'})
    return render(request,'forgot-password.html')

def profile(request):
    return render(request,'profile.html')