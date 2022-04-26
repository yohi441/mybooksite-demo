from re import template
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Cart
from mybooksite.models import Book
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from mybooksite.models import Book
from .models import Checkout
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin




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



class CheckboxCheck(LoginRequiredMixin, View):

    def get(self, request):
        return HttpResponseRedirect(reverse('carts:cart'))

    def post(self, request):
        template = 'carts/checkout.html'
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


class CartView(LoginRequiredMixin, View):
    template = "carts/cart.html"

    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        item_in_cart = get_items_in_cart(cart)
        count = cart.books.count()
        context = {
                "cart": cart,
                "count": count,
                "item_in_cart":item_in_cart
            }
    
        return render(request, self.template, context)
    


class AddToCart(View):
    template = 'carts/partials/add_to_cart_alert.html'
    template_exist = 'carts/partials/add_to_cart_book_exist.html'
    template_out_of_stock = 'carts/partials/add_to_cart_book_out_of_stock.html'
    template_error = 'carts/partials/add_to_cart_book_error.html'

    def post(self, request, pk):
        try:
            cart = Cart.objects.get(user=request.user.id)
            book = Book.objects.get(pk=pk)
            if book.is_in_stock == 'out of stock':
                return render(request, self.template_out_of_stock)
            if book in cart.books.all():
                return render(request, self.template_exist)
        except:
            return render(request, self.template_error)

        cart.books.add(book)
        count = cart.books.count()
        context = {
            'new_count':count
        }
        
        return render(request, self.template, context)



class CartItemDelete(View):
    template = 'carts/partials/partial_cart.html'

    def delete(self, request, pk):
        try:
            cart = Cart.objects.get(user=request.user.id)
            book = Book.objects.get(pk=pk)
            cart.books.remove(book)
            count = cart.books.count()
            item_in_cart = get_items_in_cart(cart)
            context = {
                'cart': cart,
                'new_count': count,
                'item_in_cart': item_in_cart
            }
            return render(request, self.template, context)
        except:
            raise Http404("Cart not found")
        
    def get(self, request, pk):

        return HttpResponseRedirect(reverse('carts:cart', args=(int(request.user.id),)))



class RecentOrder(View):
    template = 'carts/recent_order.html'

    def post(self, request):
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
        return render(request, self.template, context)

    def get(self, request):
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
        return render(request, self.template, context)



class ListOfOrders(View):
    template = 'carts/orders.html'

    def get(self, request):
        try:
            user_orders = Checkout.objects.filter(user=request.user).order_by('-created_at')
            count = get_count_cart(request)
        except:
            raise Http404("Orders not exist")
        context = {
            'user_orders': user_orders,
            'count': count
            }
        return render(request, self.template, context)



class DetailOrder(View):
    template = 'carts/list_of_order.html'

    def get(self, request, pk):
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

        return render(request, self.template, context)



class DeleteOrder(View):
    template_partial = 'carts/partials/partial_order.html'

    def delete(self, request, pk):
        try:
            order = Checkout.objects.get(pk=pk)
            order.delete()
            user_orders = Checkout.objects.filter(user=request.user).order_by('-created_at') 
        except:
            raise Http404("Order not found")
        context = {
            'user_orders': user_orders,
        }

        return render(request, self.template_partial, context)









