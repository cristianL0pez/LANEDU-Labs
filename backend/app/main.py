"""Minimal FastAPI entrypoint with a simple health check route."""
from fastapi import FastAPI

app = FastAPI(title="LANEDU Labs Backend")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint used by load balancers and monitoring."""
    return {"status": "ok"}


if __name__ == "__main__":
    # For local debugging only; in Docker use the command in the Dockerfile.
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
