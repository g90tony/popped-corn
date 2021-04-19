from flask import render_template,request,redirect,url_for
from . import main
from ..requests import get_movies,get_movie,search_movies
from .forms import ReviewForm
from ..models import Review


@main.route('/')
def index():
    
    title = "Home: Welcome to Popped-Corn: The best and honest Movie Review Platform"
    
    movie_search = request.args.get('movie_query')
    
    popular_movie = get_movies("popular")
    upcoming_movie = get_movies('upcoming')
    now_showing_movie = get_movies('now_playing')
    
    if movie_search:
        return(redirect(url_for('search', movie_name = movie_search)))
    else:
        return render_template('index.html', title= title, popular= popular_movie, upcoming = upcoming_movie, nowShowing = now_showing_movie)

@main.route('/movie/<int:id>')
def movie(id):
    
    movieData = get_movie(id)
    title = f'{movieData.title}'
    reviews = Review.get_reviews(movieData.id)
    
    return render_template('movie.html', movie=movieData, title=title, reviews = reviews)

@main.errorhandler(404)
def four0four():
    return render_template('4o4.html'),404


@main.route('/search/<movie_name>')
def search(movie_name):
    movie_search_terms = movie_name.split(' ')
    movie_search_query = "+".join(movie_search_terms)
    
    search_results = search_movies(movie_search_terms)
    title = f'Search results for {movie_name}'
    
    return render_template("movie_search.html",results = search_results, title = title )
    
    
@main.route('/movie/review/new/<int:id>', methods = ['GET', 'POST'])
def new_review(id):
    form = ReviewForm()
    movie = get_movie(id)
   
    if form.validate_on_submit():
        form_title = form.title.data
        form_review = form.review.data
        new_review = Review(movie.id,form_title,movie.poster,form_review)
        new_review.save_review() 

        return redirect(url_for('movie', id= movie.id))

    title = f'{movie.title} review'

    return render_template('review_form.html', title= title, review_form = form, movie = movie) 