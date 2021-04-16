from app import app
import urllib.request, json
from models import movie

MovieObj = movie.Movie


api_key = app.config['API_KEY']
base_url = app.config['BASE_URL']


def get_movies(category):
    get_movies_url = base_url.format(category, api_key)
    
    with urllib.request.urlopen(get_movies) as url:
        get_movies_data = url.read()
        get_movies_response = json.loads(get_movies_data)
        
    movie_results = None
    
    if get_movies_response['results']:
        movie_results_list = get_movies_response['results']
        movie_results = process_results(movie_results_list)
        
    return movie_results
