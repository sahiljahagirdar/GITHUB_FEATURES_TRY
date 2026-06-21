from fastapi import FastAPI
from src.utils.db import Base,engine
from src.Users.router import User_route
from src.Episode.router import episode_route
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from src.utils.limiter import limiter

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(User_route)
app.include_router(episode_route)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    SlowAPIMiddleware
)

@app.get('/')
def home():
    return 'COMEDY SHOWS API'