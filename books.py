from helper import types
from typing import Optional
from helper.data import books
from datetime import date
from helper.Instanse import Book
from starlette import status
from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

@app.get('/')
async def Home():
    return {
        'status': 'success',
        'message': 'Welcome to book api'
    }


@app.get('/books', response_model=list[types.BookResponse])
async def Books(
    rating: Optional[float]= Query(None, lt=6, gt=0),
    category: Optional[str]= Query(None, max_length=25, min_length=3),
    start_date: Optional[date] = Query(None, gt=date(1990,1,1)),
    end_date: Optional[date] = Query(None, lt=date(2030,1,1))
    ):
    return [book for book in books
            if (category is None or (category.casefold() == book.category.casefold()))
            and (rating is None or (book.rating >= rating))
            and (start_date is None or (book.publish_date >= start_date))
            and (end_date is None or (book.publish_date <= end_date))
            ]


@app.post('/books', response_model=types.BookResponse, status_code=status.HTTP_201_CREATED)
async def CreateBook(request_data: types.BookCreate):

    new_book = Book(**request_data.model_dump())
    new_book.id = len(books) + 1

    books.append(new_book)
    return new_book


@app.get('/books/{id}', response_model=types.BookResponse)
async def BookDetail(id:int = Path(..., gt=0)):

    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail={"message": "Book not found"})


@app.patch('/books/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def BookUpdate(id:int, request_data: types.BookUpdate):

    for book in books:
        if book.id == id:
            book_to_update = request_data.model_dump(exclude_unset=True)

            for key, value in book_to_update.items():
                setattr(book, key, value)


@app.delete('/books/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def BookDelete(id:int = Path(..., gt=0)):

    for i in range(len(books)):
        if books[i].id == id:
            books.pop(i)
            break
