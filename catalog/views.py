from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1    

    context = {
        'title' : 'Local Library',
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits' : num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog.html', context=context)

from django.views import generic

def author(request):
    return render(request, 'author.html', context=context)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2
    context_object_name = 'authors' 

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['title'] = 'Author List'
        return context

class AuthorDetailView(generic.DetailView):
    model = Author

class BookListView(generic.ListView):
    model = Book
    paginate_by = 1
    context_object_name = 'books'    # my own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='국내')[:5] # get 5 books containing the title "국내"

    # def get_queryset(self):
    #     return Book.objects.filter(genre__icontains='국내')[:5]

    def get_context_data(self, **kwargs):
        # call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to context
        context['title'] = 'Book List'
        return context

class BookGenreListView(generic.ListView):
    model = Book
    context_object_name = 'booksforgenre'    # my own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='국내')[:5] # get 5 books containing the title "국내"

    def get_queryset(self):
         return Book.objects.filter(genre__exact=self.id)[:5]

    def get_context_data(self, **kwargs):
        # call the base implementation first to get the context
        context = super(BookGenreListView, self).get_context_data(**kwargs)
        # Create any data and add it to context
        context['title'] = 'Book List'
        return context

class BookDetailView(generic.DetailView):
    model = Book

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 4

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')