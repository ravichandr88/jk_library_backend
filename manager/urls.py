
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from .views import retrieve_all_books, get_or_create_review, book_summary_and_review

urlpatterns = [
    path('books/<int:id>', retrieve_all_books),
    path('books', retrieve_all_books),
    path('books/<int:book_id>/reviews', get_or_create_review),
    path('books/<int:book_id>/summary', book_summary_and_review)
]
