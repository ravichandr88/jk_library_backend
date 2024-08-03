from django.contrib import admin
from .models import Book, Review

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'created_at')  # Fields to display in the list view
    search_fields = ('title',)  # Fields to search by

admin.site.register(Book, BookAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'rating')
    search_fields = ('rating', )

admin.site.register(Review, ReviewAdmin)
