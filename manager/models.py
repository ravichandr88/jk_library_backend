from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from asgiref.sync import sync_to_async
from django.utils import timezone

def year_choices():
    return [(r,r) for r in range(1500, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, null=False, unique=True)
    author = models.CharField(max_length=200, null=False)
    genre = models.CharField(max_length=200, null=False)
    # YearPublished field will only beable to accept values from 1500 year to today
    year_published = models.IntegerField(_('year'), choices=year_choices, default=current_year)
    summary = models.TextField(max_length=2000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"title: {self.title} | author: {self.author} | genre: {self.genre} | year_published: {self.year_published}"
    
class Review(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE ,related_name="book_reviews")
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reviews")
    user_id = models.IntegerField(validators=[MinValueValidator(1)])
    review_text = models.TextField(max_length=1000, null=False)
    # Rating field is restricted to have values between 1 to 5
    rating = models.IntegerField(_('rating'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"book_title: {self.book_id.title} | user_id: {self.user_id.first_name} | rating: {self.rating}"
        