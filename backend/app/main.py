'''This file provides a FastAPI entry point. It registers all routes and 
configures CORS (Cross-Origin Resource Sharing)'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth

app = FastAPI(
    title = "MoodWatch API",
    description= "AI-powered movie recommendation system", 
    version= "0.1.0"
)

#CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware, 
    allow_origins=[
        "http://localhost:5173"
        ], # React frontend development server (Vite)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "moodwatch-api"
    }

