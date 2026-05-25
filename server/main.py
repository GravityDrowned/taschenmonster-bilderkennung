import sys
import os

# Allow importing controller.py from the repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from server import controller

controller_index = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global controller_index
    print("Initializing nxbt controller...", flush=True)
    print("Open Change Grip/Order on your Nintendo Switch now.", flush=True)
    controller_index = controller.init()
    print("Controller connected. Server ready.", flush=True)
    yield
    print("Shutting down...", flush=True)


app = FastAPI(lifespan=lifespan)


class PlayRequest(BaseModel):
    states: List[str]


@app.get("/health")
def health():
    return {"status": "connected"}


@app.post("/play")
def play(request: PlayRequest):
    if controller_index is None:
        raise HTTPException(status_code=503, detail="Controller not initialized")
    try:
        controller.play(controller_index, request.states)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}
