import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
movies=pickle.load(open("movies_list.pkl",'rb'))
similarity=pickle.load(open("similarity.pkl",'rb'))
movies_list=movies['title'].values

st.header("Movie Recommender System")

selected_movie=st.selectbox("select a movie:" , movies_list)

import streamlit.components.v1 as components

# Function to fetch movie posters from TMDB
def fetch_poster(movie_id):
    url ="https://api.themoviedb.org/3/discover/movie/{}?api_key=e41c2d0bc77022fac5c62c56293f0650".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path=data['poster_path']
    full_path=""+poster_path
    return full_path

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distances[1:6]:  # Start from 1 to avoid recommending the movie itself
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

# Streamlit app
st.title('Movie Recommendation System')

selected_movie = st.selectbox('Select a movie:', movies_list)

if st.button("Recommend"):
    movie_name, movie_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
