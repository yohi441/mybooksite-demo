import re

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import logout, login
from django.contrib.auth import get_user_model
from accounts.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q 
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode






def login_view(request):
    template ='accounts/login.html'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')

    else:
        form = AuthenticationForm(request)
        if request.user.is_authenticated:
            return redirect('/')
    context = {
        'form':form
    }

    return render(request, template, context)


def logout_view(request):
    logout(request)

    return redirect('mybooksite:index')
    

def check_username(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        if username:
            if len(username) < 4:
                context = {
                    'msg': 'Username must have atleast 4 characters',
                    'color': 'text-red-700',
                }
                return render(request, "accounts/partials/invalid_username.html", context)
            if get_user_model().objects.filter(username=username).exists():
                context = {
                    'msg': 'Username is already exists',
                    'color': 'text-red-700',
                    }
                return render(request, "accounts/partials/invalid_username.html", context)
            else:
                context = {
                    'msg': 'Username is available',
                    'color': 'text-green-600',
                     }
                return render(request, "accounts/partials/invalid_username.html", context)
        else:
            context = {
                'msg': 'This field is required',
                'color': 'text-red-700',
                }
            return render(request, "accounts/partials/invalid_username.html", context)
    else:
        return redirect('accounts:register')


def check_email(request):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            print(email)
            if re.search(regex, email):
                context = {
                    'msg': 'Valid email',
                    'color': 'text-green-600'
                    }
                return render(request, "accounts/partials/invalid_email.html", context)
            else:
                context = {
                    'msg': 'Invalid email',
                    'color': 'text-red-700'
                    }
                return render(request,"accounts/partials/invalid_email.html", context)
        else:
            context = {
                'msg': 'This field is required',
                'color': 'text-red-700',
            }
            return render(request, "accounts/partials/invalid_email.html", context)
    else:
        return redirect('accounts:register')
        



def register_view(request):
    template = "accounts/register.html"

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mybooksite/index')  

    else:
        form = RegisterForm()
        if request.user.is_authenticated:
            return redirect('mybooksite/index')

    context = {
        'form': form
    }
    
    return render(request, template, context)



def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Password Request'
                    email_template_name = 'accounts/password_message.txt'
                    parameters = {
                        'email': user_email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'mybooksite',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject, email, '', [user.email], fail_silently=False)
                    except:
                        return HttpResponse("Invalid Header")
                    return redirect('accounts:password_reset_done')
    else:
        password_form = PasswordResetForm()

    context = {
        'password_form': password_form
    }
    return render(request, 'accounts/password_reset.html', context)
