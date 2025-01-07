from fastapi import FastAPI
import uvicorn

from app.users.router import router as users_router


app = FastAPI()

app.include_router(users_router)

@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
