from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from vex_search import ask_vex

app = FastAPI(title="VEX AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "status": "online",
        "name": "VEX AI"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
async def ask(data: Question):
    query = data.question.strip()

    if not query:
        return {"error": "Please enter a question"}

    try:
        result = await run_in_threadpool(ask_vex, query)
        return result

    except Exception as error:
        return {
            "error": "VEX AI encountered an error",
            "details": str(error)
        }
