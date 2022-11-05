from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def hello_async() -> dict[str, str]:
    return {"message": "Hello world"}


@app.get("/sync")
def hello_sync() -> dict[str, str]:
    return {"message": "Hello world"}


@app.get("/hello/{who}")
async def hello_who_async(who: int, message: str = 'hello') -> dict[str, str]:
    fake_users_db = {1: 'admin', 2: 'John'}
    user = fake_users_db.get(who, 'username')
    return {"message": f'{message}, {user}'}


class Author(BaseModel):
    name: str
    born_year: int


class Book(BaseModel):
    title: str
    author: Author
    text: Optional[str] = None


@app.post('/books')
@app.post('/books/{idx}')
async def post_book(
        book: Book
):
    return {
        'message': f"{book.author.name} wrote a great book!"
                   f"I will definitely read {book.title}"
    }
