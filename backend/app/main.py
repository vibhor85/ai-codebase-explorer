from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.repository.api import router
from app.repository.exception import InvalidRepositoryPathException

app = FastAPI(title="AI Codebase Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(InvalidRepositoryPathException)
def invalid_repository_path_exception_handler(_request: Request, exc: InvalidRepositoryPathException):
    return JSONResponse(
        status_code=400,
        content={
            "code": "INVALID_REPOSITORY_PATH",
            "message": "Repository path is invalid.",
            "path": exc.path,
        },
    )


app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "message": "Backend is healthy"}
