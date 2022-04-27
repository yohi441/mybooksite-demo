from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse
from mybooksite.models import Book, Category
from carts.views import get_count_cart
from django.views.generic import ListView, DetailView, TemplateView, View


class SearchView(View):
    template = 'components/search_results.html'

    def get(self, request):
        q = request.GET.get('q')
        count = get_count_cart(request)
        books = Book.objects.filter(title__icontains=q)[:10]
        if q.strip() == "":
            q = 'Search field is empty'
            books = None
        context = {
            'books': books,
            'q': q.strip(),
            'count': count
        }
        return render(request, self.template, context)


class IndexView(ListView):

    categories = Category.objects.all()

    template_name = "index.html"
    model = Book
    paginate_by = 10
    ordering = ['updated_at']

    def get_context_data(self, **kwargs):

        count = get_count_cart(self.request)
        context = super().get_context_data(**kwargs)
        context['mylist'] = [1, 2, 3, 4, 5]
        context['categories'] = self.categories
        context['count'] = count

        return context


class BookDetailView(DetailView):
    template_name = 'detail.html'
    model = Book
    context_object_name = 'book'
    recently_viewed_book = None

    def get_object(self):
        obj = super().get_object()

        if 'recently_viewed' in self.request.session:

            if obj.pk in self.request.session['recently_viewed']:
                self.request.session['recently_viewed'].remove(obj.pk)

            books = Book.objects.filter(
                pk__in=self.request.session['recently_viewed'])
            self.recently_viewed_book = sorted(books,
                                               key=lambda x: self.request.session['recently_viewed'].index(
                                                   x.id)
                                               )
            self.request.session['recently_viewed'].insert(0, obj.pk)

            if len(self.request.session['recently_viewed']) > 5:
                self.request.session['recently_viewed'].pop()

        else:
            self.request.session['recently_viewed'] = [obj.pk]

        self.request.session.modified = True

        return obj

    def get_context_data(self, **kwargs):

        count = get_count_cart(self.request)
        context = super().get_context_data(**kwargs)
        context['count'] = count
        context['recently_viewed_book'] = self.recently_viewed_book

        return context


class CategoryView(View):
    template = 'index.html'

    def get(self, request, pk):
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

        return render(request, self.template, context)


class AboutUsView(TemplateView):
    template_name = 'about_us.html'

    def get_context_data(self, **kwargs):

        count = get_count_cart(self.request)
        context = super().get_context_data(**kwargs)
        context['count'] = count

        return context
