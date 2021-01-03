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




# 미리 작성된 폼(RenewBookForm)을 import
from catalog.forms import RenewBookForm
# 함수 내부에서 쓰일 유용한 객체나 메소드를 import한다. 

# 해당 모델의 기본 키(primary key) 값에 연결되는 특정 객체를 반환 또는 없을 경우 Http404 예외를 발생시킨다. 
from django.shortcuts import get_object_or_404
# 특정 URL로의 재전송을 생성한다. 
from django.http import HttpResponseRedirect
# URL 설정(configuration)의 이름과 전달 인자들로 부터 URL을 만들어 낸다. 템플릿의 url 태그와 같음
from django.urls import reverse
# 날짜와 시간을 다루는 파이썬의 라이브러리
import datetime
from django.contrib.auth.decorators import permission_required

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # POST 요청이면 폼 데이터를 처리한다
    if request.method == 'POST':

        # 폼 인스턴스를 생성하고 요청에 의한 데이타로 채운다 (binding):
        # RenewBookForm: import한 폼
        book_renewal_form = RenewBookForm(request.POST)

        # 폼이 유효한지 체크한다:
        if book_renewal_form.is_valid():
            # form.cleaned_data 데이타를 요청받은대로 처리한다(여기선 그냥 모델 due_back 필드에 써넣는다)
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            print(book_instance.due_back)
            book_instance.save()

            # 새로운 URL로 보낸다:
            return HttpResponseRedirect(reverse('manage-borrowed') )

    # GET 요청 (혹은 다른 메소드)이면 기본 폼을 생성한다.
    else:
        # 기본 폼에 전달할 초기값을 만들어서 폼에 전달 (initial=() )
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
#from .models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    #initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = ['title','author','summary','isbn','genre','language']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')