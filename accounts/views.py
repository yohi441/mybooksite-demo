import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import logout, login
from django.contrib.auth import get_user_model
from django.urls import reverse
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
from carts.views import get_count_cart
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View



class MyLoginView(View):
    template = 'accounts/login.html'
    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        context = {
            'form': form,
            'count': 0
        }
        return render(request, self.template, context)


    
    def get(self, request):
        form = AuthenticationForm(request)
        if request.user.is_authenticated:
            return redirect('/')
        context = {
            'form': form,
            'count': 0
        }

        return render(request, self.template, context)



class MyLogoutView(View):
    
    def get(self, request):
        logout(request)

        return redirect('mybooksite:index')



class CheckUsername(View):

    def post(self, request):
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

    def get(self, request):
        return redirect('accounts:register')
        


class CheckEmail(View):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    def post(self, request):
        email = request.POST.get('email')
        if email:
            if re.search(self.regex, email):
                return render(request, "accounts/partials/valid_email.html")
            else:
                return render(request,"accounts/partials/invalid_email.html")
        else:          
            return render(request, "accounts/partials/invalid_email_field_required.html")
    
    def get(self, request):
        return redirect('accounts:register')



class MyRegisterView(View):
    template = "accounts/register.html"

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:register_success')
        
        context = {
            'form': form,
            'count':0
        }
        return render(request, self.template, context)

    def get(self, request):
        form = RegisterForm()
        if request.user.is_authenticated:
            return redirect('mybooksite:index')

        context = {
            'form': form,
            'count':0
        }
        return render(request, self.template, context)



class PasswordResetRequest(View):

    def post(self, request):
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
                        'domain': 'booksite-demo.herokuapp.com',
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
        context = {
            'password_form': password_form
        }
        return render(request, 'accounts/password_reset.html', context)

    def get(self, request):
        password_form = PasswordResetForm()
        context = {
            'password_form': password_form
        }
        return render(request, 'accounts/password_reset.html', context)



class ProfileView(LoginRequiredMixin, View):
    template = 'profile.html'
    
    def get(self, request):
        count = get_count_cart(request)

        context = {
            'count': count
        }

        return render(request, self.template, context)



class ProfileEdit(View):
    template = "accounts/partials/edit_profile.html"
    template_full = "accounts/edit_profile_full.html"

    def post(self, request):
        instance = Profile.objects.get(user=request.user)

        form = ProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            instance.user.first_name = first_name
            instance.user.last_name = last_name
            instance.user.email = email
            instance.user.save()
            form.save()
            return HttpResponseRedirect(reverse('accounts:profile'))
        count = get_count_cart(request)
        context = {
            'form': form,
            'count': count
            }
        return render(request, self.template_full, context)

    def get(self, request):
        form = ProfileForm()
        count = get_count_cart(request)

        if request.htmx:
            return render(request, self.template, { 'form': form })
        return render(request, self.template_full, { 'form': form, 'count': count })



class RegisterSuccess(View):
    template = 'register_success.html'

    def get(self, request):
        if request.user.is_authenticated:
            HttpResponseRedirect(reverse('mybooksite:index'))
        return render(request, self.template)





    


