from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from asgiref.sync import sync_to_async

from .models import Book, Review 
from .async_tasks import fetch_books_loop, save_book_instance, get_the_book, delete_book_object, get_all_reviews, save_review, avg_rating_of_book
import asyncio
from asgiref.sync import async_to_sync, sync_to_async

from .serializers import BookSerializer, ReviewSerializers
from django.forms.models import model_to_dict
from .helper import validate_other_than_already_exists_error
import traceback

@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_all_books(request, id=None):
    '''
    This is both list all books and also filter based on id API
    id: book id that we want to find, if id id None, we return all the books list

    If id is not found, we return error message.
    method GET: We list all the books if the ID is None.
    method POST: We will create a Bok instance.
        request-body:{
            "title": "good morning", 
            "author": "ravi", 
            "genre":"music", 
            "year_published":"1990", 
            "summary":"Very good morning"
            }
    method PUT: We will retrieve the book-object if present 
                Validate the given data using BookSerializers 
                But we will eliminate all the errors that include "already exists", since we are trying to update model this error is not meaningful
                When there are no errors , we will call async save() function.
    method DELETE: Since we already got the object, just call async delete function
    '''
    if request.method == "GET":
        params = {}
        if id is not None:
            params['id'] = id
        # async task for fetching books list
        books = asyncio.run(fetch_books_loop(**params)).values()
        if id is not None and len(books) == 0:
            return Response(data={"message": "No book found with the given ID"}, status=400)
        return Response(data=books[0], status=200)
    # If method used is POST, we create a BOOK instance
    elif request.method == "POST":
        book = BookSerializer(data=request.data)
        # check if the provided data is valid
        if book.is_valid():    
            # async DB operation to save the row in table
            asyncio.run(save_book_instance(book))
            return Response(data={"status":"success"}, status=200)
        # If the data provided is not valid, then return error message
        return Response(book.errors, status=400)
    # Since, we use "id" in both PUT and DELETE, lets validate it first 
    # But validate it only when it is not a None
    book_obj = None
    if id is not None:
        book_obj = asyncio.run(get_the_book(id))
    elif book_obj is None:
        return Response(data={"message": "Internal Server Error"}, status=500)
    # If Book with given ID is not found return error
    if isinstance(book_obj, tuple):
        return Response(data={"message": book_obj[0]}, status=400)
    # Update part of the code          
    elif request.method == "PUT":
        # handle missing id here
        if id is None:
            return Response(data={"message": "Please provide an ID of the Book to update"}, status=400)
        try:
            # if we got the Book instance, update it with given fields
            book_dict = BookSerializer(book_obj).data
            try:
                for field, value in request.data.items():
                    book_dict[field] = value
            except KeyError as e:
                print(f"Unknown field {e} found while trying to update Book instance")
                return Response(data={"message": f"Unknown field {e} for updating Book"}, status=400)
            # If all fields are good, now validate values using serializer and save if it is valid
            updated_book = BookSerializer(data=book_dict)
            errors_found = validate_other_than_already_exists_error(updated_book)
            if not errors_found:
                for key, value in book_dict.items():
                    setattr(book_obj, key, value)
                asyncio.run(save_book_instance(book_obj))
                return Response(data={"status": "updated"}, status=200)
            else:
                # if the serialized object is not valid, return the error messages
                return Response(data=errors_found, status=400)
        except Exception as e:
            print(f"Exception while fetching the book using ID, to update: {traceback.format_exc()}")
            return Response({"message": "Internal Server Error"}, status=500)
    # Code to delete
    else:
        asyncio.run(delete_book_object(book_obj))
        return Response(data={"status": "deleted"}, status=200)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_or_create_review(request, book_id=None):
    '''
    This function will retrieve reviews and adds a review to the given book-id
    method GET: returns all the reviews related to the book-id
    method POST: create review for th given book-id
    request-body: 
            {
            "review_text": "good book",
            "rating": 90, 
            "user_id": 2
            }
    '''
    # First check whether the book_id is valid or not
    if book_id is None:
        return Response({"message": "Please provide a Book-ID"}, status=400)
    # Check with Table to find the book object
    book_obj = None
    if book_id is not None:
        book_obj = asyncio.run(get_the_book(book_id))
    elif book_obj is None:
        return Response(data={"message": "Internal Server Error"}, status=500)
    # If Book with given ID is not found return error
    if isinstance(book_obj, tuple):
        return Response(data={"message": book_obj[0]}, status=400)
    # Code to return list of reviews of a book
    if request.method == "GET":
        reviews = asyncio.run(get_all_reviews(**{"book_id": book_obj})).values()
        return Response(data=reviews)
    # Code to add a review
    else:
        data = request.data
        # Add book-id as we have already validated book-object
        data['book_id'] = book_obj.id
        review_form = ReviewSerializers(data=data)
        if review_form.is_valid():
            asyncio.run(save_review(review_form))
            return Response(data={'status': 'created'}, status=200)
        return Response(data={"message": review_form.errors}, status=400)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_summary_and_review(request, book_id=None):
    '''
    '''
    # First check whether the book_id is valid or not
    if book_id is None:
        return Response({"message": "Please provide a Book-ID"}, status=400)
    # Check with Table to find the book object
    book_obj = None
    if book_id is not None:
        book_obj = asyncio.run(get_the_book(book_id))
    elif book_obj is None:
        return Response(data={"message": "Internal Server Error"}, status=500)
    # If Book with given ID is not found return error
    if isinstance(book_obj, tuple):
        return Response(data={"message": book_obj[0]}, status=400)
    # Get average of all the ratings of the book 
    avg_rating = asyncio.run(avg_rating_of_book(book_obj))["rating__avg"]
    return Response(data={
        "summary": book_obj.summary,
        "rating": avg_rating
        })



