import logging
from fastapi import FastAPI
from app.api.authors import router as authors_router
from app.api.categories import router as categories_router
from app.api.books import router as books_router
from app.api.users import router as user_router
from app.api.issues import router as issue_router
from app.middleware import request_logging_middleware
from app.api.admins import router as admins_router
from app.api.auth import router as auth_router

app = FastAPI(title="Library Management System")

# basic logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

app.middleware("http")(request_logging_middleware)

app.include_router(authors_router)
app.include_router(categories_router)
app.include_router(books_router)
app.include_router(user_router)
app.include_router(issue_router)
app.include_router(admins_router)
app.include_router(auth_router)