from fastapi import FastAPI
from src.utils.db import Base,engine

Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
def home():
    return 'COMEDY SHOWS API'