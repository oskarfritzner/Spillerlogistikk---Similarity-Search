import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def find_similar_outfield_players(player_name, dataset, feature_list, weights_dict=None, top_n=5):
    """
    Finds the top N most similar outfield players to the given player using cosine similarity.

    Args:
        player_name (str): Name of the reference player (must be exact match in 'short_name' column)
        dataset (DataFrame): Cleaned DataFrame with only outfield players and selected features
        feature_list (list): List of features used for similarity calculation
        weights_dict (dict): Dictionary of weights per feature (e.g. role profile). Keys = feature names
        top_n (int): Number of similar players to return

    Returns:
        DataFrame: Top N most similar players
    """

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(dataset[feature_list])

    # Apply weights if a profile is given (e.g., CAM, CB, etc.)
    if weights_dict:
        weights = np.array([weights_dict.get(f, 0.0) for f in feature_list])
        X_scaled = X_scaled * weights

    # Get the player index
    player_index = dataset[dataset["short_name"] == player_name].index

    if player_index.empty:
        print(f"Player '{player_name}' not found in dataset.")
        return pd.DataFrame()

    # Calculate cosine similarity
    similarities = cosine_similarity(X_scaled[player_index], X_scaled).flatten()

    # Create result DataFrame
    similarity_df = dataset[["short_name"]].copy()
    similarity_df["similarity"] = similarities

    # Remove the player themselves
    similarity_df = similarity_df[dataset["short_name"] != player_name]

    # Return top N
    return similarity_df.sort_values(by="similarity", ascending=False).head(top_n)