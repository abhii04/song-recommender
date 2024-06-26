import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd

# Load your dataset
df = pd.read_csv('spotify_tracks_dataset.csv')

# Create CountVectorizer
count_vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','))

# Fit and transform the genre data
count_matrix = count_vectorizer.fit_transform(df['track_genre'])

# Fit NearestNeighbors model
nn_model = NearestNeighbors(metric='cosine', algorithm='brute')
nn_model.fit(count_matrix)


def get_recommendations(song_name, df=df, nn_model=nn_model, count_vectorizer=count_vectorizer):
    if df.loc[df['track_name'] == song_name].empty:
        st.error(f"Song '{song_name}' not found in the database.")
        return []

    input_genre_vector = count_vectorizer.transform([df.loc[df['track_name'] == song_name, 'track_genre'].values[0]])
    distances, indices = nn_model.kneighbors(input_genre_vector)
    recommendations = df.iloc[indices[0]].drop_duplicates(subset='track_name')['track_name'].values.tolist()

    return recommendations


def main():
    st.title('Song Recommendation App')

    # Input for song name
    song_name = st.text_input('Enter a song name:')

    if st.button('Get Recommendations'):
        if song_name:
            recommendations = get_recommendations(song_name)
            st.write(f"Recommendations for '{song_name}':")
            st.write("1. " + "\n2. ".join(recommendations))
        else:
            st.write('Please enter a song name.')

    st.image('play.png', caption='Listen', use_column_width=True)


if __name__ == '__main__':
    main()
