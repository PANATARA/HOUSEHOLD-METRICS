from fastapi import APIRouter, FastAPI
import uvicorn

# import routs
from chores_completions.routs import router as chores_completions_router

app = FastAPI()

main_api_router = APIRouter(prefix="/api")

main_api_router.include_router(
    chores_completions_router, prefix="", tags=["Chore completion"]
)

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
