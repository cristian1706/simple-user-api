"""
Main FastAPI application instance.

This module sets up the FastAPI application with all routes and middleware.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import auth, users
from app.core.config import settings
from app.core.rate_limiter import limiter
from app.db.session import create_tables

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A simple user management API",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Add rate limiter middleware only if not in testing mode
if not settings.TESTING:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(
    users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"]
)


@app.get("/")
async def root(request: Request):
    """
    Root endpoint that renders the registration page.
    
    Args:
        request: The incoming request
        
    Returns:
        TemplateResponse: The rendered registration page
    """
    return templates.TemplateResponse("register.html", {"request": request})


@app.on_event("startup")
async def startup_event():
    """
    Actions to run on application startup.
    """
    # Create database tables
    create_tables()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
