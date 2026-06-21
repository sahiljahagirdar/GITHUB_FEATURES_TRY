from fastapi import FastAPI
from src.utils.db import Base,engine
from src.Users.router import User_route
from src.Episode.router import episode_route

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(User_route)
app.include_router(episode_route)

@app.get('/')
def home():
    return 'COMEDY SHOWS API'