from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, calorie_log, exercise, weight, workout_log

app = FastAPI(
    title="Personal Project API",
    description="筋トレ・競馬収支・予算管理 API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(weight.router)
app.include_router(exercise.router)
app.include_router(workout_log.router)
app.include_router(calorie_log.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
