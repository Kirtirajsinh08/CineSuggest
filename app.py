import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API")

def fetch_movie_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&&language=en-US'.format(movie_id, api_key))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def movie_recommender_system(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_movie_poster(movie_id))
    return recommended_movies, recommended_movies_posters

dictionary_of_movies = pickle.load(open('movies_dictionary.pkl', 'rb'))
movies = pd.DataFrame(dictionary_of_movies)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown('### CineMatch - A Personalised Movie Recommender🍿')

selected_movie_name = st.selectbox(
    'Select the last movie you saw', movies['title'].values
)

if st.button('Recommend Movies'):
    recommendations, posters = movie_recommender_system(selected_movie_name)
    
    column1, column2, column3, column4, column5 = st.columns(5)

    with column1:
        st.text(recommendations[0])
        st.image(posters[0])
    
    with column2:
        st.text(recommendations[1])
        st.image(posters[1])

    with column3:
        st.text(recommendations[2])
        st.image(posters[2])

    with column4:
        st.text(recommendations[3])
        st.image(posters[3])

    with column5:
        st.text(recommendations[4])
        st.image(posters[4])
    