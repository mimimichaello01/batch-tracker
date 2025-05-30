from fastapi import FastAPI

from app.infra.api.batch_router import batch_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="The system of control of production tasks",
        docs_url="/api/docs",
        debug=True
    )
    app.include_router(batch_router)

    return app


