
from django.http import Http404, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Cart
from mybooksite.models import Book
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from mybooksite.models import Book
from .models import Checkout




def get_count_cart(request):

    if request.user.is_authenticated:

        cart = Cart.objects.get(user=request.user)

        count = cart.books.count()

        return count

    return 0




def get_items_in_cart(cart):

    item_in_cart = []

    for item in cart.books.all():

        item_in_cart.append(item.id)

    return item_in_cart

@login_required
def checkbox_check(request):

    template = 'carts/checkout.html'

    if request.method == "POST":

        checks = request.POST.getlist('checks')

        books = Book.objects.filter(id__in=checks)

        count = get_count_cart(request)

        total = 0

        for book in books:

            total += book.price

        context = {

            'books':books,

            'count': count,

            "total": total
        }

        return render(request, template, context)

    return HttpResponseRedirect(reverse('carts:cart'))



@login_required
def cart_view(request):

    template = "carts/cart.html"

    cart = Cart.objects.get(user=request.user)

    item_in_cart = get_items_in_cart(cart)


    count = cart.books.count()

    context = {
            "cart": cart,

            "count": count,

            "item_in_cart":item_in_cart
        }
    
    return render(request, template, context)




@require_http_methods(["POST"])
def add_to_cart(request, pk):

    template = 'carts/partials/add_to_cart_alert.html'

    template_exist = 'carts/partials/add_to_cart_book_exist.html'

    template_out_of_stock = 'carts/partials/add_to_cart_book_out_of_stock.html'

    template_error = 'carts/partials/add_to_cart_book_error.html'

    
    try:
        cart = Cart.objects.get(user=request.user.id)

        book = Book.objects.get(pk=pk)

        if book.is_in_stock == 'out of stock':

            return render(request, template_out_of_stock)

        if book in cart.books.all():

            return render(request, template_exist)

    except:

        return render(request, template_error)

    cart.books.add(book)

    count = cart.books.count()
    
    context = {

        'new_count':count

    }
    
    return render(request, template, context)

    

    # return HttpResponseRedirect(reverse('carts:cart', args=(int(request.user.id),)))




@login_required
def cart_item_delete(request, pk):

    template = 'carts/partials/partial_cart.html'

    if request.method == "DELETE":

        try:

            cart = Cart.objects.get(user=request.user.id)

            book = Book.objects.get(pk=pk)

            cart.books.remove(book)

            count = cart.books.count()

            item_in_cart = get_items_in_cart(cart)

            print(item_in_cart)

            context = {

                'cart': cart,

                'new_count': count,

                'item_in_cart': item_in_cart

            }

            return render(request, template, context)
            
        except:

            raise Http404("Cart not found")
            
    return HttpResponseRedirect(reverse('carts:cart', args=(int(request.user.id),)))


def recent_order(request):

    template = 'carts/recent_order.html'

    if request.method == "POST":

        checkout = Checkout.objects.create(user=request.user)

        try:

            list_id = request.POST.getlist('books')

            books = Book.objects.filter(id__in=list_id)

            total = 0

            for book in books:

                checkout.books.add(book)

                total += book.price

            checkout.total = total

            checkout.save()

            list_of_books = checkout.books.all()

            count = get_count_cart(request)

        except:

            raise Http404("User not found")

        context = {

            'total':total,

            'list_of_books':list_of_books,

            'count': count,

            'recent_order': checkout
        }
        
        
        return render(request, template, context)

    else:

        try:

            orders = Checkout.objects.filter(user=request.user)

            recent_order = orders.order_by('-created_at')[0]

            list_of_books = recent_order.books.all()

            total = recent_order.total

            count = get_count_cart(request)
        
        except:

            raise Http404("Recent Order not found")

        context = {

                'total':total,

                'list_of_books':list_of_books,

                'count': count,

                'recent_order':recent_order

            }

        return render(request, template, context)



def list_of_orders(request):

    template = 'carts/orders.html'
    
    try:
        user_orders = Checkout.objects.filter(user=request.user).order_by('-created_at')

        count = get_count_cart(request)

    except:

        raise Http404("Orders not exist")
    
    context = {

        'user_orders': user_orders,

        'count': count
    }

    return render(request, template, context)


def detail_order(request, pk):

    template = 'carts/list_of_order.html'

    try:

        recent_order = Checkout.objects.get(pk=pk)

        list_of_books = recent_order.books.all()

        count = get_count_cart(request)

        total = recent_order.total
    
    except:

        raise Http404("Order not found")
        

    context = {

        'total':total,

        'list_of_books':list_of_books,

        'count': count,

        'recent_order':recent_order

    }

    return render(request, template, context)


def delete_order(request, pk):

    template_partial = 'carts/partials/partial_order.html'

    if request.method == 'DELETE':

        try:

            order = Checkout.objects.get(pk=pk)

            order.delete()

            user_orders = Checkout.objects.filter(user=request.user).order_by('-created_at')
           
        except:

            raise Http404("Order not found")
        
        context = {

            'user_orders': user_orders,

        }

        return render(request, template_partial, context)

    # return HttpResponseRedirect(reverse('carts:orders'))







