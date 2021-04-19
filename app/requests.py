import urllib.request,json
from .models import Movie


api_key = None
base_url = None


MovieObj = Movie
def configure_request(app):
    global api_key,base_url
    api_key = app.config['API_KEY']
    base_url = app.config['BASE_URL']

def process_results(movie_list):
    movie_results = list()
    
    for movie_item in movie_list:
        id = movie_item.get("id")
        title = movie_item.get("title")   
        overview = movie_item.get("overview")    
        poster = movie_item.get("poster_path")  
        vote_average = movie_item.get("vote_average")    
        vote_count = movie_item.get("vote_count")  
        
        if poster:
            newMovieInstance = MovieObj(id,title,overview,poster,vote_average,vote_count)
            movie_results.append(newMovieInstance)
    return movie_results


def get_movies(category):
    get_movies_url = base_url.format(category, api_key)
    
    with urllib.request.urlopen(get_movies_url) as url:
        get_movies_data = url.read()
        get_movies_response = json.loads(get_movies_data)
        
    movie_results = None
    
    if get_movies_response['results']:
        movie_results_list = get_movies_response['results']
        movie_results = process_results(movie_results_list)
   
    return movie_results


def get_movie(id):
    get_movie_data_url = base_url.format(id, api_key)
    
    with urllib.request.urlopen(get_movie_data_url) as url:
        movie_response = url.read()
        movie_response_data = json.loads(movie_response)
        
        movie_object = None
        
        if movie_response_data:
            id = movie_response_data.get('id')
            title = movie_response_data.get('title')
            overview = movie_response_data.get('overview')
            poster = movie_response_data.get('poster_path')
            vote_average = movie_response_data.get('vote_average')
            vote_count = movie_response_data.get('vote_count')
            
            movie_object = MovieObj(id, title, overview, poster, vote_average, vote_count)
            
        return movie_object


def search_movies(movie_name):
    search_movie_url = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(api_key,movie_name)
    with urllib.request.urlopen(search_movie_url) as url:
        search_movie_response = url.read()
        search_movie_data = json.loads(search_movie_response)
        
        search_results = None 
        
        if search_movie_data['results']:
            search_movie_list = search_movie_data['results']
            search_results = process_results(search_movie_list)
            
    return search_results
        