import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st

sns.set(style="whitegrid")
# Load the datasets
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Preview
print("🎥 Movies")
print(movies.head())
print("⭐ Ratings")
print(ratings.head())

# Merge ratings and movies
df = pd.merge(ratings, movies, on="movieId")
df.head()

# Create pivot table (movies as rows, users as columns)
movie_user_matrix = df.pivot_table(index="title", columns="userId", values="rating")
movie_user_matrix.head()

# Fill missing values with 0
movie_user_matrix_filled = movie_user_matrix.fillna(0)

# Compute cosine similarity between movies
cos_sim = cosine_similarity(movie_user_matrix_filled)

# Create similarity dataframe
cos_sim_df = pd.DataFrame(cos_sim, index=movie_user_matrix.index, columns=movie_user_matrix.index)
cos_sim_df.head()

# Function to get similar movies
def get_similar_movies(movie_name, top_n=3):
    similar_scores = cos_sim_df[movie_name].sort_values(ascending=False)
    return similar_scores[1:top_n+1]

# Test with a sample movie
get_similar_movies("The Matrix (1999)", 3)

####################################

# Load the data
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
df = pd.merge(ratings, movies, on="movieId")

# Create pivot table
movie_user_matrix = df.pivot_table(index="title", columns="userId", values="rating")
movie_user_matrix_filled = movie_user_matrix.fillna(0)

# Compute similarity
cos_sim = cosine_similarity(movie_user_matrix_filled)
cos_sim_df = pd.DataFrame(cos_sim, index=movie_user_matrix.index, columns=movie_user_matrix.index)

# Streamlit app
st.title("🎬 Saudi Movie Recommender")
st.write("Recommend similar movies based on user ratings")

# Movie selection
selected_movie = st.selectbox("Choose a movie:", movie_user_matrix.index)

# Number of recommendations
top_n = st.slider("Number of similar movies to show:", 1, 10, 3)

# Recommend movies
if st.button("Recommend"):
    similar_scores = cos_sim_df[selected_movie].sort_values(ascending=False)
    recommended = similar_scores[1:top_n+1]
    st.subheader(f"Movies similar to '{selected_movie}':")
    for movie, score in recommended.items():
        st.write(f"**{movie}** — Similarity Score: {score:.2f}")