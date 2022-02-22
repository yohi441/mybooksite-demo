from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.urls import reverse
from mybooksite.models import Book, Category
from carts.models import Cart
from carts.views import get_count_cart



def search_view(request):

    template = "components/search_results.html"

    count = get_count_cart(request)

    try:

        q = request.GET.get('q')

        books = Book.objects.filter(title__contains=q)[:10]
 
    except:

        q = None

    context = {

        'books': books,

        'q': q,

        'count': count,
    }

    if q == "":

        context = {

        'q': q,

        'count': count,

    }

        q = "Search field is empty"

        return render(request, template, context)

    return render(request, template, context)


def index_view(request):

    template = "index.html"

    count = get_count_cart(request)
    
    categories = Category.objects.all()

    books = Book.objects.all().order_by('updated_at')

    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    
        
    context = {

        'mylist': [1,2,3,4,5],

        "categories": categories,

        "page_obj": page_obj,

        "count": count,

    }

    return render(request, template, context) 


def detail_view(request, pk):

    template = "detail.html"

    count = get_count_cart(request)

    book = get_object_or_404(Book, pk=pk)

    recently_viewed_book = None

    if 'recently_viewed' in request.session:

        if pk in request.session['recently_viewed']:

            request.session['recently_viewed'].remove(pk)

        books = Book.objects.filter(pk__in=request.session['recently_viewed'])
        
        recently_viewed_book = sorted(books,

            key=lambda x: request.session['recently_viewed'].index(x.id)

            )

        request.session['recently_viewed'].insert(0, pk)
        
        if len(request.session['recently_viewed']) > 5:

            request.session['recently_viewed'].pop()

    else:

        request.session['recently_viewed'] = [pk]

    request.session.modified = True

    context = {

        'book': book,

        'recently_viewed_book': recently_viewed_book,

        'count': count
    }

    return render(request, template, context)


def category_view(request,pk):

    template ="index.html"

    count = get_count_cart(request)

    categories = Category.objects.all()

    category = Category.objects.get(pk=pk)

    books = category.books.all()

    paginator = Paginator(books, 10)
    
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {

        "categories": categories,

        "count": count,
        
        "page_obj": page_obj,
    }

    return render(request, template, context) 


def about_us_view(request):

    template = "about_us.html"

    count = get_count_cart(request)
 
    context = {
        'count':count
    }
    
    return render(request, template, context)







    





