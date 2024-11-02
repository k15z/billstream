import fastapi
from api.example_service import router
from api.weather_service import router as weather_router

app = fastapi.FastAPI(
    title="Agent Toolkit",
    summary="Enable AI agents to pay for tool use in real-time.",
)

app.include_router(router)
app.include_router(weather_router)