from re import template
from django.http import HttpResponse, request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Cart
from mybooksite.models import Book
from django.urls import reverse
from django.contrib.auth.decorators import login_required



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
    cart = Cart.objects.get(user=request.user.id)

    try:
        book = Book.objects.get(pk=pk)
        if book in cart.books.all():
            HttpResponse("book is already in cart")
    except:
        pass
    
    cart.books.add(book)

    return HttpResponseRedirect(reverse('carts:cart', args=(int(request.user.id),)))