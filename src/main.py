# src/main.py

from fastapi import FastAPI
from src.config.settings import Settings
from src.api import chat, document, user

app = FastAPI(title="Multi-Agent Chatbot", version="1.0.0")

# Load settings
settings = Settings()

# Include routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(document.router, prefix="/document", tags=["document"])
app.include_router(user.router, prefix="/user", tags=["user"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Multi-Agent Chatbot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)