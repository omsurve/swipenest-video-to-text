from app.routes.upload import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

@app.get("/")
def home():
    return {"message": "API is running"}
