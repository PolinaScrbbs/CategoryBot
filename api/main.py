from fastapi import FastAPI

from .auth.router import router as authRouter
from .category.router import router as categoryRouter
from .test.router import router as testRouter

app = FastAPI(
    title="Deyana Sinema",
    description="The API of a Big Cinema for Very Big Kittens",
    version="2.2.8",
)

app.include_router(authRouter, tags=["Auth"])
app.include_router(categoryRouter, tags=["Category"])
app.include_router(testRouter, tags=["Test"])
