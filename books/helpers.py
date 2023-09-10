import requests


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

    return data["volumeInfo"]
