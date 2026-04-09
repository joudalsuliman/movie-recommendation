# tmdb_helper.py
import requests

API_KEY = "eef7828b97c5860253a6eff11d60ab45"
BASE_URL = "https://api.themoviedb.org/3"

def search_movie(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": query
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def get_recommendations(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/recommendations"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def get_poster_url(path):
    return f"https://image.tmdb.org/t/p/w500{path}" if path else ""

# app.py
import streamlit as st
from tmdb_helper import search_movie, get_recommendations, get_poster_url

st.title("🎬 Movie Recommendation System")

search_query = st.text_input("🔎 Search for a movie")

if search_query:
    results = search_movie(search_query)
    if not results:
        st.warning("❌ No movies found.")
    else:
        selected = results[0]  # take first result
        st.subheader(f"🎥 {selected['title']} ({selected.get('release_date', '')[:4]})")
        st.image(get_poster_url(selected['poster_path']), width=200)
        st.write(selected.get('overview', 'No description available.'))

        st.markdown("### 📍 Recommended Movies:")
        recommendations = get_recommendations(selected['id'])
        for movie in recommendations[:5]:
            st.write(f"**{movie['title']}** ({movie.get('release_date', '')[:4]})")
            st.image(get_poster_url(movie['poster_path']), width=150)
