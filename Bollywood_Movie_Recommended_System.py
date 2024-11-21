
import difflib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

# Load the pre-trained model
model = load_model('movie_recommendation_system_lstm.keras')

# Assuming `df` is your movie dataset, load it from a CSV
df = pd.read_csv(r"C:\Users\Abhishek\Desktop\project done\movie_rm_s\updated_bollywood_movies.csv")

# Function to correct spelling
def correct_spelling(input_string, possible_values):
    close_matches = difflib.get_close_matches(input_string.lower(), possible_values, n=1)
    return close_matches[0] if close_matches else input_string

# Function to recommend movies based on various criteria
def recommend_movies(movie_name, genre, casting, year_of_release, year_range, top_n):
    # Ensure the 'year_of_release' is treated as numeric
    df['year_of_release'] = pd.to_numeric(df['year_of_release'], errors='coerce')

    # Initialize the filtered DataFrame based on initial filters
    df_filtered = df

    # Filter based on movie name if provided
    if movie_name:
        df_filtered = df_filtered[df_filtered['movie_name'].str.contains(movie_name, case=False, na=False)]

    # Filter based on genre if provided
    if genre:
        df_filtered = df_filtered[df_filtered['genre'].str.contains(genre, case=False, na=False)]

    # Filter based on casting if provided
    if casting:
        df_filtered = df_filtered[df_filtered['cast'].str.contains(casting, case=False, na=False)]

    # Filter based on year of release if provided
    if year_of_release:
        df_filtered = df_filtered[df_filtered['year_of_release'] == year_of_release]

    # Filter based on year range if provided
    if year_range:
        df_filtered = df_filtered[(df_filtered['year_of_release'] >= year_range[0]) & 
                                  (df_filtered['year_of_release'] <= year_range[1])]

    # Here, you can replace this with actual predictions from the model (mock predictions used)
    predictions = np.random.rand(df_filtered.shape[0])  # Mock predictions

    # Add predictions to the filtered DataFrame for display
    df_filtered['predictions'] = predictions

    # Sort by predictions and return the top N
    return df_filtered.nlargest(top_n, 'predictions')


def interactive_recommendation():
    while True:
        # Ask user for inputs one by one
        movie_name = input("Enter movie name (or leave blank): ")
        genre = input("Enter genre (or leave blank): ")
        casting = input("Enter casting (or leave blank): ")
        year_of_release = input("Enter year of release (or leave blank): ")
        
        # Convert year_of_release to int if provided
        if year_of_release:
            try:
                year_of_release = int(year_of_release)
            except ValueError:
                year_of_release = None

        # Ask for year range if desired
        year_range_input = input("Enter year range (e.g., 2000-2010) or leave blank: ")
        if year_range_input:
            try:
                year_range = list(map(int, year_range_input.split('-')))
            except ValueError:
                year_range = None
        else:
            year_range = None

        # Get top recommendations
        top_10 = recommend_movies(movie_name, genre, casting, year_of_release, year_range, top_n=10)
        if top_10.empty:
            print("No suitable recommendations found based on your search.")
        else:
            print("Top 10 Movie Recommendations:")
            print(top_10)

        # Ask if user wants more recommendations
        response = input("Would you like to see more recommendations? (yes/no): ").strip().lower()
        if response == 'yes':
            top_20 = recommend_movies(movie_name, genre, casting, year_of_release, year_range, top_n=20)
            print("Top 20 Movie Recommendations:")
            print(top_20)

            response = input("Would you like to see even more recommendations? (yes/no): ").strip().lower()
            if response == 'yes':
                top_50 = recommend_movies(movie_name, genre, casting, year_of_release, year_range, top_n=50)
                print("Top 50 Movie Recommendations:")
                print(top_50)
            else:
                print("ok....I will glad to help you again....Thank you!")
        elif response == 'no':
            print("ok....I will glad to help you again....Thank you!")
        else:
            print("ok....I will glad to help you again....Thank you!")
            break

# Call the function if needed for interactive session
# interactive_recommendation()
