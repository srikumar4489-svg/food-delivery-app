from django.urls import path
from .views import *

urlpatterns = [
    path('', register_view, name="register"),
    path('otp-verify/', otp_verify, name="otp_verify"),
    path('log/',log,name='home'),
    path('login/', login_view, name="login"),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-reset-otp/', verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', reset_password, name='reset_password'), 
]