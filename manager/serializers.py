from rest_framework import serializers
from .models import Book, Review

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'genre', 'year_published', 'summary')
        read_only_fields = ('created_at', 'updated_at')  # Prevent modification of these fields

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'review_text', 'rating', 'user_id', 'book_id')
        read_only_fields = ('created_at', 'updated_at')  # Prevent modification of these fields


        