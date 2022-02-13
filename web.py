from fastapi import FastAPI

from src.resource.carbon_monoxide import views

app = FastAPI()
app.include_router(views.router)