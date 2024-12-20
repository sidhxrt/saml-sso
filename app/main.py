from fastapi import FastAPI
from app.routers.saml import router as saml_router

app = FastAPI()

# Include SAML Router
app.include_router(saml_router, prefix="/saml")

@app.get("/")
async def root():
    return {"message": "Welcome to SAML SSO Integration"}