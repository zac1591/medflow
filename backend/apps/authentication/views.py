from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib import auth
from django.urls import reverse
from .utils import account_activation_token

from django.utils.encoding import force_bytes, force_text, \
    DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading


# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # get user data
        # validate
        # create user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'field_values': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 8:
                    messages.error(request, 'Password too short!')
                    return render(request, 'authentication/register.html',
                                  context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path to view
                # getting domain we're on
                # relative url to verification
                # encode uid
                # token

                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                    'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://' + current_site.domain + link

                email = EmailMessage(
                    email_subject,
                    'Hi ' + user.username + ', Please the link below to activate your account \n' + activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                EmailThread(email).start()
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect(
                    'login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'The email is invalid'},
                                status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry email already taken'},
                                status=409)

        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({
                                    'username_error': 'User should only contain alphanumeric characters'},
                                status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {'username_error': 'Sorry username already taken'}, status=409)

        return JsonResponse({'username_valid': True})


class PasswordValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']

        if len(str(password)) < 8:
            return JsonResponse({
                                    'password_error': 'Password must be at least 8 characters long'},
                                status=400)

        __esp_char = '!@#$%^&*()-+?_=,<>/'

        if not any(c in __esp_char for c in str(password)):
            return JsonResponse({
                                    'password_error': 'Your password must contain at least one of the symbols: !@#$%^&*()-+?_=,<>/'},
                                status=400)

        return JsonResponse({'password_valid': True})


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username + ' you are now logged in')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials, please try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):

        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'The email provided is not valid')
            return render(request, 'authentication/reset-password.html',
                          context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():
            email_body = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password', kwargs={
                'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Reset your password'

            reset_url = 'http://' + current_site.domain + link

            email = EmailMessage(
                email_subject,
                'Hi ' + user[
                    0].username + ', Please use the link below to reset your password \n' + reset_url,
                'noreply@semycolon.com',
                [email],
            )
            EmailThread(email).start()

        messages.success(request,
                         'We have sent you an email to reset your password')

        return render(request, 'authentication/reset-password.html')


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request,
                              'Password link has expired, please request a new one.')
                return render(request, 'authentication/reset-password.html')

        except Exception as identifier:
            messages.info(request, 'Something went wrong, please try again.')
            return render(request, 'authentication/reset-password.html')

        return render(request, 'authentication/set-newpassword.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords dont match')
            return render(request, 'authentication/set-newpassword.html',
                          context)

        if len(password) < 6:
            messages.error(request, 'Password too short')
            return render(request, 'authentication/set-newpassword.html',
                          context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,
                             'Password changed successfully, please login using your new password')

            return redirect('login')

        except Exception as identifier:
            messages.info(request, 'Something went wrong, pleae try again.')
            return render(request, 'authentication/set-newpassword.html',
                          context)