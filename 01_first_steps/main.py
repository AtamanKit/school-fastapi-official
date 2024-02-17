from fastapi import FastAPI

app = FastAPI()


# A simple get request
@app.get("/")
async def root():
    return {"message": "Hello World"}


# A get request with a parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
