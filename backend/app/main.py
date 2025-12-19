"""FastAPI application entrypoint."""
from fastapi import FastAPI

from app.routers.auth_router import router as auth_router
from app.routers.labs_router import router as labs_router
from app.routers.progress_router import router as progress_router
from app.routers.ranking_router import router as ranking_router
from app.routers.users_router import router as users_router

app = FastAPI(title="LANEDU Labs Backend")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint used by load balancers and monitoring."""
    return {"status": "ok"}


# TODO: Replace fake auth dependencies in routers with real JWT/OAuth2 security.
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(labs_router)
app.include_router(progress_router)
app.include_router(ranking_router)


if __name__ == "__main__":
    # For local debugging only; in Docker use the command in the Dockerfile.
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
