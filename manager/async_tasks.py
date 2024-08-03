
from .models import Book, Review 
from asgiref.sync import sync_to_async
from .serializers import BookSerializer
import traceback
from django.contrib.auth.models import User 
from django.db.models import Avg
# from channels.db import database_sync_to_async

async def fetch_books_loop(**kwargs):
    results = await sync_to_async(Book.objects.filter, thread_sensitive=True)(**kwargs)
    return results

async def save_book_instance(serialized_object):
    try:
        await sync_to_async(serialized_object.save, thread_sensitive=True)()
    except Exception as e:
        print(f"Exception while creating book: {traceback.format_exc()}")

async def get_the_book(id):
    '''
    Try to fetch the Book with given ID, and return the Book object
    id: book id
    if there is no book with given ID, then return error message
    if there is an unknown exception, return None
    '''
    try:
        return await sync_to_async(Book.objects.get, thread_sensitive=True)(**{"id": id})
    except Book.DoesNotExist as e:
        print(f"Book with provided ID not found")
        return ("Book with given ID not found", )
    except Exception as e:
        print(f"Exception while fetching a book: {traceback.format_exc()}")
    
async def save_book_changes(book_obj):
    try:
        await sync_to_async(book_obj.save, thread_sensitive=True)()
    except Exception as e:
        print(f"Exception while creating book: {traceback.format_exc()}")

async def delete_book_object(book_obj):
    try:
        await sync_to_async(book_obj.delete, thread_sensitive=True)()
    except Exception as e:
        print(f"Exception while deleting a book: {traceback.format_exc()}")

async def get_all_reviews(**kwargs):
    return await sync_to_async(Review.objects.filter, thread_sensitive=True)(**kwargs)

async def save_review(review_obj):
    return await sync_to_async(review_obj.save, thread_sensitive=True)()

async def avg_rating_of_book(book_obj):
    return await sync_to_async(book_obj.book_reviews.aggregate)(Avg('rating'))

