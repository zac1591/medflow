from django.urls import path
from .views import RegistrationView, LoginView, CompletePasswordReset, ResetPasswordView, UsernameValidationView, EmailValidationView, PasswordValidationView, VerificationView, LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('validate-password', csrf_exempt(PasswordValidationView.as_view()), name='validate-password'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset-password', ResetPasswordView.as_view(), name='request-password'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-user-password')
]