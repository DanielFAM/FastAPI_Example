from fastapi import Depends, FastAPI, Body, Path, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
#documentado con Swagger

app = FastAPI()
app.title = "My app with FastAPI"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) :
        auth = await super().__call__(request)
        data  = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid credentials")

class User(BaseModel):
    email:str
    password:str

#Used for resume the input of values in object
class Movie(BaseModel):
    id: Optional[int] | None  = None
    title: str = Field(min_length=5, max_length=15) #validate object parameters with Field
    overview: str = Field(min_length=15, max_length=50)
    year:int = Field(le=2023)
    rating:float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "title":"My movie",
                "overview":"Film description",
                "year":2022,
                "rating":9.8,
                "category":"Acción"
            }
        }

movies = [
    {
        "id":1,
        "title":"Avatar",
        "overview":"",
        "year":"2009",
        "rating":7.8,
        "category":"Acción"
    },
    {
        "id":2,
        "title":"Avatar 2",
        "overview":"",
        "year":"2009",
        "rating":7.8,
        "category":"Acción"
    }
]


@app.get('/', tags=['home'])
def home():
    return HTMLResponse('<h1>Hello World</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)


@app.get('/movies',tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


#Path parameters
@app.get('/movies/{id}',tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie: #validate path parameters with Path
    for item in movies:
        if item["id"] == id:
            return JSONResponse(status_code=200, content=item)
    return JSONResponse(status_code=404, content=[])

#query parameters
@app.get('/movies/', tags={'movies'}, response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:

    data = [item for item in movies if item['category'] == category]

    return JSONResponse(content=data)


@app.post('/movies', tags={'movies'}, response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message":"movie succesfully created"})


@app.put('/movies/{id}', tags={'movies'}, response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(status_code=200, content={"message":"movie succesfully updated"})


@app.delete('/movies/{id}',tags={'movies'},response_model=dict, status_code=200)
def delete_movie(id: int ) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message":"movie succesfully deleted"})