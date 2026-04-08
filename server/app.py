from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
from env import EthicalHackerEnv

from contextlib import asynccontextmanager

# Global environment instance initialized once
_env = EthicalHackerEnv(task_id="hard")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the core environment cleanly inside the active loop
    await _env.reset()
    yield

app = FastAPI(title="Ethical Hacker Env API", lifespan=lifespan)

class StepRequest(BaseModel):
    action: Any
    task_id: Optional[str] = None

@app.get("/")
@app.get("/health")
def health_check():
    """Health check endpoint for HF Spaces and automated pings."""
    return {"status": "healthy", "env": "ethical-hacker-v1"}

@app.post("/reset")
async def reset(task_id: str = "hard"):
    """
    Resets the environment for a specific task.
    Returns standard OpenEnv reset response shape.
    """
    global _env
    _env = EthicalHackerEnv(task_id=task_id)
    obs = await _env.reset()
    return {
        "observation": obs.model_dump(),
        "reward": 0.0,
        "done": False,
        "info": {"status": "initialized", "task_id": task_id}
    }

@app.post("/step")
async def step(request: StepRequest):
    """
    Executes a single step in the environment.
    Ensures zero unwanted print statements in production routes.
    """
    try:
        obs, reward, done, info = await _env.step(request.action)
        return {
            "observation": obs.model_dump(),
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        # Avoid leaking full stack traces; return cleaned error message
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state")
def get_state():
    """Returns the internal state snapshot for validation."""
    return _env.state()

def main():
    """Entry point for the OpenEnv benchmark orchestrator."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860, workers=1)

if __name__ == "__main__":
    main()
