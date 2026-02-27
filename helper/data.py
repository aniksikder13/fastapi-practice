from datetime import date
from .Instanse import Book

books = [
    Book(
        1,
        "Computer Science Pro",
        "Coding with Ruby",
        "Computer Science",
        5,
        "An advanced guide covering algorithms, data structures, and system design.",
        39.99,
        date(2021,6,25)
    ),
    Book(
        2,
        "Be Fast with FastAPI",
        "Coding with RGB",
        "Web Development",
        5,
        "Learn how to build high-performance APIs using FastAPI and Python.",
        29.99,
        date(2017,3,20)
    ),
    Book(
        3,
        "Master Endpoints",
        "Coding with Ruby",
        "API Development",
        4,
        "A practical guide to designing clean, scalable REST APIs.",
        34.50,
        date(2023,6,28)
    ),
    Book(
        4,
        "Harry Potter and the Philosopher's Stone",
        "J.K. Rowling",
        "Fantasy",
        5,
        "The magical story of a young wizard discovering his destiny.",
        24.99,
        date(2022,6,8)
    ),
    Book(
        5,
        "Clean Code",
        "Robert C. Martin",
        "Software Engineering",
        5,
        "A handbook of agile software craftsmanship and best coding practices.",
        42.00,
       date(2008,10,13)
    )
]
