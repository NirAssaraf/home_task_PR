from fastapi import FastAPI

from api.routes.base import BaseRouter
app = FastAPI()
apiRouter = BaseRouter()
apiRouter.include_routes()

app.include_router(apiRouter.get_router(), tags=['api'], prefix='/api')


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "App is runing!"}
