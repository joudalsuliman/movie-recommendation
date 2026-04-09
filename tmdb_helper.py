import requests

API_KEY = "eef7828b97c5860253a6eff11d60ab45"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def search_movie(query):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": query
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def get_recommendations(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def get_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return "https://via.placeholder.com/150"

def get_popular_movies():
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def get_movie_details(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()