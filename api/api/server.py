import fastapi
from api.example_service import router

app = fastapi.FastAPI(
    title="Billstream",
    summary="Streaming payments for agentic interactions.",
)

app.include_router(router)
