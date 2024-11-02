import fastapi
from api.alpaca_service import router as alpaca_router
from api.greeting_service import router as greeting_router
from api.weather_service import router as weather_router
from api.nytimes_service import router as nytimes_router
from api.linkedin_service import router as linkedin_router
from api.calendar_service import router as calendar_router
from api.wikipedia_service import router as wikipedia_router

app = fastapi.FastAPI(
    title="Agent Toolkit",
    summary="Enable AI agents to pay for tool use in real-time.",
)

app.include_router(greeting_router)
app.include_router(weather_router)
app.include_router(nytimes_router)
app.include_router(linkedin_router)
app.include_router(alpaca_router)
app.include_router(calendar_router)
app.include_router(wikipedia_router)
