from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', views.login_page, name='login'),
    path('register', views.register, name='register'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('user_page', views.user_page, name='user_page'),
    path('verify_otp_page/<int:user_id>/', views.verify_otp_page, name='verify_otp_page'),
    path('resend_verify_email/<int:user_id>/', views.resend_verify_email, name='resend_verify_email'),

]
