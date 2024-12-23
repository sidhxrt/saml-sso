from fastapi import FastAPI
from app.routers.saml import router as saml_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(saml_router, prefix="/saml")

@app.get("/")
async def root():
    return {"message": "Welcome to SAML SSO Integration"}
