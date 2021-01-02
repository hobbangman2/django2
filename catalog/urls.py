from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='catalog'),
    path('books/', views.BookListView.as_view(), name='books'),
    # path('books/genre/<id>/', views.BookGenreListView.as_view(), name='books-genre'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
] 