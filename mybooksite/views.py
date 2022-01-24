
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from mybooksite.models import Book, Category
from carts.models import Cart



def search_view(request):
    template = "index.html"

    try:
        q = request.GET.get('q')
    except:
        q = None

    books = Book.objects.filter(title__contains=q)

    context = {
        'books': books,
        'q': q
    }

    if q == '':
        return redirect('mybooksite/index')

    return render(request, template, context)


def index_view(request):
    template = "index.html"

    categories = Category.objects.all()
    books = Book.objects.all()
    paginator = Paginator(books, 10)
    

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "categories": categories,
        "page_obj": page_obj
    }

    return render(request, template, context) 


def detail_view(request, pk):
    template = "detail.html"

    book = Book.objects.get(pk=pk)
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
        'recently_viewed_book': recently_viewed_book
    }

    return render(request, template, context)


def category_view(request,pk):
    template ="index.html"

    categories = Category.objects.all()
    category = Category.objects.get(pk=pk)
    books = category.books.all()

    paginator = Paginator(books, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        
        "page_obj": page_obj
    }

    return render(request, template, context) 


def about_us_view(request):
    template = "about_us.html"

    

    return render(request, template)



