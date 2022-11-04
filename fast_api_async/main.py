from fastapi import FastAPI

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
