import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(
    page_title="CineMatch - AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        color: #f0f6fc;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #ff4b4b, #ff7676, #ffa4a4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-top: 8px;
    }

    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(255, 75, 75, 0.2);
        border-color: rgba(255, 75, 75, 0.5);
    }

    .movie-title {
        font-weight: 600;
        font-size: 0.9rem;
        color: #ffffff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-top: 6px;
    }

    .movie-meta {
        font-size: 0.78rem;
        color: #f1c40f;
        margin-top: 4px;
    }

    div.stButton > button:first-child {
        background: linear-gradient(90deg, #e50914, #b20710);
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.65rem 2rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
        width: 100%;
        transition: all 0.3s ease;
    }

    div.stButton > button:first-child:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6);
        color: white;
    }

    .stImage img {
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id, title):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=3)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass

    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key=8265bd1679663a7ea12ac168da84d2e8&query={title}"
        response = requests.get(search_url, timeout=3)
        data = response.json()
        results = data.get('results', [])
        if results and results[0].get('poster_path'):
            return f"https://image.tmdb.org/t/p/w500{results[0]['poster_path']}"
    except Exception:
        pass

    return "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&auto=format&fit=crop&q=60"

def recommend(movie_name):
    index = movies[movies['title'] == movie_name].index[0]
    
    if isinstance(similarity, dict):
        movie_indices = similarity[index]
    else:
        distances = similarity[index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        movie_indices = [i[0] for i in movies_list]

    recommended_movies = []
    for idx in movie_indices:
        row = movies.iloc[idx]
        poster_url = fetch_poster(row['id'], row['title'])
        recommended_movies.append({
            'title': row['title'],
            'poster': poster_url,
            'rating': row.get('vote_average', 0.0),
            'genres': row.get('parsed_genres', '')
        })
    return recommended_movies

st.markdown('<div class="hero-title">🎬 CineMatch AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Discover high-rated movies personalized with Machine Learning</div>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2.5, 1])

with col_center:
    selected_movie = st.selectbox(
        "🔎 Search or Select a Movie:",
        options=movies['title'].values,
        index=0
    )
    st.write("")
    btn_recommend = st.button("🍿 Recommend Similar Movies")

if btn_recommend:
    with st.spinner("Finding best matching movies..."):
        results = recommend(selected_movie)

    st.write("")
    st.markdown(f"### 🎯 Top 5 Movies For You:")
    
    cols = st.columns(5, gap="medium")

    for i in range(5):
        with cols[i]:
            st.image(results[i]['poster'], use_container_width=True)
            rating_text = f"⭐ {results[i]['rating']:.1f}/10" if results[i]['rating'] > 0 else "⭐ N/A"
            genre_text = results[i]['genres'][:25] + '...' if len(results[i]['genres']) > 25 else results[i]['genres']
            st.markdown(f"""
            <div class="movie-card">
                <div class="movie-title" title="{results[i]['title']}">{results[i]['title']}</div>
                <div class="movie-meta">{rating_text}</div>
                <div style="font-size:0.75rem; color:#8b949e; margin-top:2px;">{genre_text}</div>
            </div>
            """, unsafe_allow_html=True)
