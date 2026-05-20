from fastapi import FastAPI
from routers import tareas as tareas_router

app = FastAPI(
    title="API de Tareas",
    description="API REST para gestionar tareas con FastAPI y Pydantic",
    version="1.0"
)

app.include_router(tareas_router.router)