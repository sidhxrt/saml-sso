from fastapi import FastAPI
from app.routers.saml import router as saml_router

app = FastAPI()

app.include_router(saml_router)

@app.get("/")
async def root():
    return {"message": "hello saml-sso"}