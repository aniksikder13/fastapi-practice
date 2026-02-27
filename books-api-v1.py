from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class BookType(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    category: str
    publish_date: str
    rating: float

class BookListType(BaseModel):
    success: bool
    total: int
    data: list[BookType]

class CreateBookType(BaseModel):
    success: bool
    message: str
    data: BookType

class BookUpdateType(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    publish_date: Optional[str] = None


books = [
    {"id": 1, "title": "The Time-Traveling Tacos", "author": "Professor Burrito", "category": "Science Fiction", "publish_date": "2020-05-12", "rating": 4.8},
    {"id": 2, "title": "Math for Wizards", "author": "Merlin Numbers", "category": "Magic & Math", "publish_date": "2019-11-03", "rating": 4.5},
    {"id": 3, "title": "History of Dragons", "author": "Professor Burrito", "category": "Fantasy History", "publish_date": "2018-07-21", "rating": 4.7},
    {"id": 4, "title": "Quantum Banana Theory", "author": "Dr. Peelstein", "category": "Science Comedy", "publish_date": "2021-02-14", "rating": 4.2},
    {"id": 5, "title": "Adventures in Noodle Land", "author": "Chef Spaghettius", "category": "Cooking & Travel", "publish_date": "2020-08-09", "rating": 4.3},
    {"id": 6, "title": "The Great Pillow War", "author": "Captain Snooze", "category": "Comedy", "publish_date": "2022-01-01", "rating": 4.6},
    {"id": 7, "title": "Ghosts of Pizza Past", "author": "Mozzarella Moon", "category": "Paranormal Comedy", "publish_date": "2017-10-31", "rating": 4.1},
    {"id": 8, "title": "The Secret Life of Spoons", "author": "Spooner McFork", "category": "Kitchen Mysteries", "publish_date": "2019-03-12", "rating": 4.0},
    {"id": 9, "title": "Coding with Unicorns", "author": "Rainbow Bytes", "category": "Programming Fantasy", "publish_date": "2021-06-18", "rating": 4.9},
    {"id": 10, "title": "Pirates vs. Ninjas: The Spreadsheet", "author": "Excel McSwash", "category": "Adventure Comedy", "publish_date": "2018-12-05", "rating": 4.4},
    {"id": 11, "title": "The Invisible Sandwich", "author": "Chef Phantom", "category": "Comedy", "publish_date": "2020-09-09", "rating": 4.2},
    {"id": 12, "title": "How to Train Your Llama", "author": "Llamuel Jackson", "category": "Animal Training", "publish_date": "2022-03-22", "rating": 4.7},
    {"id": 13, "title": "Secrets of the Sock Drawer", "author": "Captain Laundry", "category": "Mystery Comedy", "publish_date": "2019-07-14", "rating": 4.3},
    {"id": 14, "title": "Adventures of a Flying Teapot", "author": "Sir Whistlepuff", "category": "Fantasy Adventure", "publish_date": "2021-11-11", "rating": 4.6},
    {"id": 15, "title": "101 Ways to Talk to Plants", "author": "Botany Bob", "category": "Gardening & Humor", "publish_date": "2020-04-20", "rating": 4.5},
]

app = FastAPI()

@app.get('/')
async def Home():
    return {"message": "FastAPI is ready to use."}


@app.get('/books', response_model=BookListType)
async def Books(
    author: Optional[str] = None,
    category: Optional[str] = None
    ):

    filtered_books = [
        book for book in books
        if(not author or (author.casefold()==book['author'].casefold()))
            and
          (not category or (category.casefold()==book['category'].casefold()))
        ]

    return {
        'success': True,
        'total': len(filtered_books),
        'data': filtered_books
    }


@app.post('/books', response_model=CreateBookType)
async def CreateBook(new_book:BookType):
    book = new_book.model_dump()
    book["id"] = len(books) + 1
    books.append(book)

    return {
        'success': True,
        'message': "Created successfully",
        'data': book
    }

@app.get('/books/{id}', response_model=BookType)
async def BookDetail(id:int):
    for book in books:
        if id == book['id']:
            return book
    return {"message": "This book is not found"}

@app.patch('/books/{id}', response_model=CreateBookType)
async def UpdateBook(id:int, update_book:BookUpdateType):

    for book in books:
        if book['id'] == id:
            update_req = update_book.model_dump(exclude_unset=True)

            for key, value in update_req.items():
                book[key] = value

            return {
                'success': True,
                'message': "Updated successfully",
                'data': book
            }

    return {
        'success': False,
        'message': "Updated Failed",
        'data': update_book.model_dump()
    }


@app.delete('/books/{id}', response_model=CreateBookType)
async def DeleteBook(id:int):

    for book in books:
        if book['id'] == id:
            books.remove(book)

            return {
                'success': True,
                'message': "Book delete successfully",
                'data': book
            }

    return {
        'success': False,
        'message': "Failed to delete Book",
    }
