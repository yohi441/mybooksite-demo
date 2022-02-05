import http
from re import template
from django.http import HttpResponse, request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Cart
from mybooksite.models import Book
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template import loader



@login_required(login_url='accounts/login')
def cart_view(request, pk):
    template = "carts/cart.html"

    cart = Cart.objects.get(user=pk)
    count = 0
    total = 0
    for item in cart.books.all():
        total += item.price
        count += 1
    cart.total = float(total)
    cart.save()
    context = {
            "cart": cart,
            "total": total,
            "count": count
        }
    
    return render(request, template, context)




@login_required(login_url='accounts/login')
def add_to_cart(request, pk):
    template = 'carts/partials/add_to_cart_alert.html'
    template_exist = 'carts/partials/add_to_cart_book_exist.html'
    template_error = 'carts/partials/add_to_cart_book_error.html'
    try:
        cart = Cart.objects.get(user=request.user.id)
        book = Book.objects.get(pk=pk)

        if book in cart.books.all():
            return render(request, template_exist)

    except:
        return render(request, template_error)

    cart.books.add(book)
    count = cart.books.count()
    
    if request.method == "POST":
        return render(request, template, {'new_count':count})

    

    # return HttpResponseRedirect(reverse('carts:cart', args=(int(request.user.id),)))




@login_required(login_url='accounts:login')
def cart_item_delete(request, pk):
    template = 'carts/partials/partial_cart.html'

    if request.method == "DELETE":
        try:
            cart = Cart.objects.get(user=request.user.id)
            book = Book.objects.get(pk=pk)
            cart.books.remove(book)
            count = cart.books.count()

            context = {
                'cart': cart,
                'new_count': count,
            }

            return render(request, template, context)
            
        except:
            HttpResponse("Error occured please try again")
            
    return HttpResponseRedirect(reverse('carts:cart', args=(int(request.user.id),)))


