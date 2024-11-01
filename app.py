import streamlit as st
import pickle
import requests

# Load movie data and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

# Dropdown for movie selection
selectvalue = st.selectbox("Select a movie from the dropdown", movies_list)

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f7d3d5cab5d9b363a246a53c5a03413a&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to fetch where the movie is available for streaming
def fetch_streaming_services(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/watch/providers?api_key=f7d3d5cab5d9b363a246a53c5a03413a".format(movie_id)
    data = requests.get(url).json()
    if 'results' in data and 'US' in data['results']:  # assuming US region
        services = data['results']['US'].get('flatrate', [])
        providers = [service['provider_name'] for service in services]
        return providers if providers else ["Not available on streaming platforms."]
    return ["Streaming information not found."]

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    recommend_streaming = []
    
    for i in distance[1:6]:  # top 5 recommendations
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
        recommend_streaming.append(fetch_streaming_services(movie_id))
    
    return recommend_movie, recommend_poster, recommend_streaming

# Button to display recommendations
if st.button("Show Recommendations"):
    movie_name, movie_poster, movie_streaming = recommend(selectvalue)
    for i in range(5):  # Display top 5 recommended movies
        st.text(movie_name[i])
        st.image(movie_poster[i])
        st.text("Available on: " + ", ".join(movie_streaming[i]))
