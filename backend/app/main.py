from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import auth, routes, websocket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(routes.router)
app.include_router(websocket.router)
