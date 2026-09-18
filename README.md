# 🎬 Movie Recommender System

A machine learning web application that recommends movies based on content similarity, built using Python, Scikit-Learn, and Streamlit.

---

## 📌 Project Overview
When you watch a movie you like, finding similar movies can take a lot of searching. This project solves that problem by using **Content-Based Filtering** to recommend the top 5 most similar movies based on:
- Movie Titles
- Story Overviews (Plot Synopsis)
- Genres

It also connects live with **The Movie Database (TMDB) API** to fetch official high-resolution posters and ratings in real-time.

---

## 🔄 How the Project Works (End-to-End Workflow)

### 1. Data Cleaning & Preparation
- We started with a dataset of movies containing titles, genres, overviews, ratings, and popularity.
- Dropped duplicates and handled missing values in text columns.
- Extracted genre names from JSON strings.
- Combined `title`, `genres`, and `overview` into a single combined feature column called `tags`.

### 2. Natural Language Processing (NLP)
- Lowercased all text to ensure uniformity.
- Removed punctuation and non-alphanumeric characters.
- Removed common English stopwords (like *the*, *is*, *in*) using NLTK.
- Applied **WordNet Lemmatization** to convert words into their root dictionary form.

### 3. Vectorization & Cosine Similarity
- Used **TF-IDF Vectorizer** (Term Frequency - Inverse Document Frequency) to convert the text tags into numerical feature vectors.
- Calculated **Cosine Similarity** between movie vectors to measure how close each movie is in content to all other movies.
- Precomputed and saved the similarity mapping into optimized, lightweight `.pkl` files.

### 4. Interactive Web Application (Streamlit)
- Built an interactive user interface using **Streamlit**.
- Users can select or search for any movie from the dropdown.
- Upon clicking **"Recommend"**, the app displays the top 5 most similar movies in a clean 5-column layout.
- High-definition posters are retrieved dynamically using TMDB API.

---

## 🛠️ Technologies Used

- **Programming Language:** Python 3.10+
- **Data Processing:** Pandas, NumPy
- **Machine Learning & NLP:** Scikit-Learn, NLTK
- **Frontend / Web Framework:** Streamlit
- **External API:** TMDB (The Movie Database) API
- **Model Storage:** Pickle

---

## 🚀 Run

1. Clone the repository:
```bash
https://movie-recommender-system-czrrfqyvautqrb4rhojqzb.streamlit.app/
