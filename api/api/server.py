import fastapi
from api.greeting_service import router as greeting_router
from api.weather_service import router as weather_router
from api.nytimes_service import router as nytimes_router

app = fastapi.FastAPI(
    title="Agent Toolkit",
    summary="Enable AI agents to pay for tool use in real-time.",
)

app.include_router(greeting_router)
app.include_router(weather_router)
app.include_router(nytimes_router)
