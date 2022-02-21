from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

@app.get('/')
def MainPageIntro():
    return PlainTextResponse("Welcome!/nHave a nice day!")