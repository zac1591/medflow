from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.urls import reverse
from .utils import token_generator

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        #get user data
        #validate
        #create user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'field_values': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password)<8:
                    messages.error(request, 'Password too short!')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username= username, email= email)
                user.set_password(password)
                user.is_active = False
                user.save()

                #path to view
                #getting domain we're on
                #relative url to verification
                #encode uid
                #token

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain

                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

                email_subject = 'Activate your account'

                activate_url = f'http://{domain}{link}'

                email_body = f'Hi {user.username}, please use this link to verify your account \n {activate_url}'

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@xppable.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')
       
        return render(request, 'authentication/register.html')



class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            print(ex)

        return redirect('login')



class EmailValidationView (View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'The email is invalid'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry email already taken'}, status=409)

        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'User should only contain alphanumeric characters'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username already taken'}, status=409)

        return JsonResponse({'username_valid': True})


class PasswordValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']

        if len(str(password)) < 8:
            return JsonResponse({'password_error': 'Password must be at least 8 characters long'}, status=400)

        __esp_char = '!@#$%^&*()-+?_=,<>/'

        if not any(c in __esp_char for c in str(password)):
            return JsonResponse({'password_error': 'Your password must contain at least one of the symbols: !@#$%^&*()-+?_=,<>/'}, status=400)

        return JsonResponse({'password_valid': True}) 


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')


class SetNewPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/set-newpassword.html')