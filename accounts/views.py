from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .authentication import EmailBackend
from .otp_utils import verify_otp
from .forms import RegisterForm
from .models import User, OtpToken

# Create your views here.

def register(request):
    register_form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.username = user.first_name + '_' + user.last_name
            email_otp = OtpToken.objects.create(expires_at=timezone.now() + timezone.timedelta(minutes=5))
            user.email_otp = email_otp
            user.save()

            send_mail(
                'Email Verification OTP',
                f'Your OTP for email verification is: {email_otp.otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return redirect('verify_otp_page', user_id=user.id)

    return render(request, 'accounts/register.html', {'form': register_form})

def verify_otp_page(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        input_email_otp = request.POST['email_otp']

        if verify_otp(user.email_otp, input_email_otp):
            user.is_email_verified = True
            user.email_otp.delete()
            user.email_otp = None
            user.save()

            login(request, user, backend='accounts.authentication.EmailBackend')
            return redirect(user_page)
        else:
            return render(request, 'accounts/verify_otp.html', {'errors': 'Entered code invalid or expired!'})


    return render(request, 'accounts/verify_otp.html')

@require_POST
def resend_verify_email(request, user_id):
    user = User.objects.get(id=user_id)

    otp_token = user.email_otp
    otp_token.delete()

    email_otp = OtpToken.objects.create(expires_at=timezone.now() + timezone.timedelta(minutes=5))
    user.email_otp = email_otp

    user.save()

    send_mail(
        'Email Verification OTP',
        f'Your OTP for email verification is: {email_otp.otp}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return JsonResponse({'success': True})
    

def login_page(request):
    if request.method == 'POST':
        user = EmailBackend.authenticate(ModelBackend(), request=request, email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user, backend='accounts.authentication.EmailBackend')
            return redirect(user_page)
    
    return render(request, 'accounts/login.html')

def logout_page(request):
    return render(request, 'accounts/logout_page.html')

@login_required()
def user_page(request):
    user = request.user
    user_addresses = user.orderaddress_set.all()
    user_orders = user.order_set.all()


    context = {
        'user': user, 
        'user_addresses': user_addresses,
        'user_orders': user_orders,
    }

    return render(request, 'accounts/user_page.html', context)
