import random
from itertools import chain

import requests

from books.models import Bookmark, History, Review


def search_books(query):
    res = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q={query}&key=AIzaSyDz5HKDZj3UX-oKP1tRMfczCXzZFRdaDM8"
    )
    data = res.json()

    return data["items"]


def search_book(query):
    res = requests.get(
        f"https://www.googleapis.com/books/v1/volumes/{query}?key=AIzaSyDz5HKDZj3UX-oKP1tRMfczCXzZFRdaDM8"
    )
    data = res.json()
    data["volumeInfo"]["id"] = data["id"]
    print(data["volumeInfo"]["id"])

    return data["volumeInfo"]


def book_recommendation():
    # Sample list of books to recommend from
    books_to_recommend = search_books("python")

    # Sample user behavior data (replace this with your actual data)
    bookmarks = Bookmark.objects.all()
    history = History.objects.all()
    reviews = Review.objects.all()

    # Combine all user behavior into a single list
    user_behavior = list(chain(bookmarks, history, reviews))

    # Filter out books the user has already interacted with
    user_books = set(item.book_id for item in user_behavior)
    print(user_books)

    temp_books = []

    # Display the recommended books
    for b in user_books:
        print(f"Recommendation: {b}")
        temp_books.append(search_book(b))

    random_sample = search_books("python")

    # Display the recommended books
    for b in random_sample:
        print(f"Recommendation: {b}")
        b["volumeInfo"]["id"] = b["id"]
        temp_books.append(b["volumeInfo"])

    books = random.choices(temp_books, k=10)

    return books
