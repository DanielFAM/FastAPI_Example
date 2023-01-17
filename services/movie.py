from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():

    def __init__(self, db):
        self.db = db

    def get_movies(self):
        result  = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result

    def get_movie_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie : Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
    
    def update_movie(self, id: int, data: MovieModel):
        
        movie = MovieService(self.db).get_movie(id)
        
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        
        self.db.commit()
    
    def delete_movie(self, movie: MovieModel):
        self.db.delete(movie)
        self.db.commit()