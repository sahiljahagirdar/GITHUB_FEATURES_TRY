from fastapi import FastAPI
from src.utils.db import Base,engine
from src.Users.router import User_route
from src.Episode.router import episode_route
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.utils.limiter import limiter
from fastapi.responses import JSONResponse

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(User_route)
app.include_router(episode_route)


async def custom_rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "message": "Too many requests. Please try again later."
        }
    )

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    custom_rate_limit_handler
)

app.add_middleware(
    SlowAPIMiddleware
)

@app.get('/')
def home():
    return 'COMEDY SHOWS API'