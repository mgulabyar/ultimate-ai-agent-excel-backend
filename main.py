from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import agent_routes
import uvicorn

app = FastAPI(title="Supreme Excel Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_routes.router)


@app.get("/")
def home():
    return {"status": "Agent Backend Online"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8007)
