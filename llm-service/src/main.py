import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer

# Get configuration from environment
ROOT_PATH = os.getenv("ROOT_PATH", "")

class TextInput(BaseModel):
    text: str

ml_models = {}

@asynccontextmanager
async def lifespan(_: FastAPI):
    ml_models['transformer'] = SentenceTransformer(os.environ["MODEL_NAME"])
    yield
    ml_models.clear()

app = FastAPI(
    title="LLM Service",
    version="1.0.0",
    root_path=ROOT_PATH,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.post("/embed")
def embed_text(input: TextInput):
    embedding = ml_models['transformer'].encode([input.text])[0].tolist()
    return JSONResponse({"embedding": embedding})

@app.get("/health", tags=["Health"])
async def health():
    """Liveness probe: only checks if app is running."""
    return JSONResponse({"status": "ok"})