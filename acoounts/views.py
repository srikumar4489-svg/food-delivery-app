import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def register_view(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already registered")
            return redirect('register')

        # OTP generate
        otp = random.randint(100000, 999999)

        # store data in session (temporary)
        request.session['name'] = name
        request.session['email'] = email
        request.session['password'] = password
        request.session['otp'] = str(otp)

        # send email
        send_mail(
            "Your OTP Code",
            f"Your OTP is {otp}",
            "srikumar1122610@gmail.com",
            [email],
            fail_silently=False,
        )

        return redirect('otp_verify')

    return render(request, "register.html")


def otp_verify(request):

    if request.method == "POST":

        user_otp = request.POST.get('otp')
        real_otp = request.session.get('otp')

        if str(user_otp) == str(real_otp):

            name = request.session.get('name')
            email = request.session.get('email')
            password = request.session.get('password')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            login(request, user)

            return redirect('customer_home')
        
        else:
            return render(request, 'otp_verify.html', {
                'error': 'Invalid OTP'
            })

    return render(request, 'otp_verify.html')

# def otp_verify(request):

#     if request.method == "POST":

#         # get OTP from form
#         user_otp = request.POST.get('otp')

#         # get real OTP from session
#         real_otp = request.session.get('otp')

#         # check OTP safely
#         if str(user_otp) == str(real_otp):

#             # get stored user details
#             name = request.session.get('name')
#             email = request.session.get('email')
#             password = request.session.get('password')

#             # create user
#             if email and password:
#                 User.objects.create_user(
#                     username=email,
#                     email=email,
#                     password=password
#                     first_name=name
#                 )

#                 login(request, user)

#             # redirect to customer home page
#             return redirect('customer_home')

#         # wrong OTP case
#         return render(request, "otp_verify.html", {
#             'error': 'Invalid OTP'
#         })

#     return render(request, "otp_verify.html")


def log(request):
    return render(request,'index.html')

def login_view(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        # Django normally uses username, so email use panna username=email store pannanum
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('customer_home')

        else:
           return render(request,'login.html',{'error':"Invalid Email or Password"})
    
    return render(request,'login.html')

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:
            User.objects.get(email=email)

            otp = random.randint(100000, 999999)

            request.session['reset_email'] = email
            request.session['reset_otp'] = str(otp)

            send_mail(
                "Password Reset OTP",
                f"Your OTP is {otp}",
                "yourmail@gmail.com",
                [email],
                fail_silently=False
            )

            return redirect('verify_reset_otp')

        except User.DoesNotExist:
            return render(request, "forgot_password.html",{"error": "Email not registered"})

    return render(request, "forgot_password.html")

def verify_reset_otp(request):

    if request.method == "POST":

        user_otp = request.POST.get("otp")
        real_otp = request.session.get("reset_otp")

        if user_otp == real_otp:
            return redirect('reset_password')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, "verify_reset_otp.html")

def reset_password(request):

    if request.method == "POST":

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:

            email = request.session.get("reset_email")

            user = User.objects.filter(email=email).first()

            if not user:
                messages.error(request,"user not found")
                return redirect('forgot_password')

            user.set_password(password1)
            user.save()

            messages.success(request,
                             "Password changed successfully")

            return redirect('login')

        else:
            messages.error(request,
                           "Passwords do not match")

    return render(request, "reset_password.html")