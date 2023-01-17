from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.login import login_router
#documentado con Swagger

app = FastAPI()
app.title = "My app with FastAPI"
app.version = "0.0.1"


app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(login_router)


base.metadata.create_all(bind=engine)


@app.get('/', tags=['home'])
def home():
    return HTMLResponse('<h1>Hello World</h1>')
