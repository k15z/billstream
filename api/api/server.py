import fastapi
from api.example_service import router

app = fastapi.FastAPI()
app.include_router(router)
