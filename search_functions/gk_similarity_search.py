import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def find_similar_goalkeepers(keeper_df, X_keeper_scaled, target_name, top_n=5):
    """
    Find the most similar goalkeepers to a target player based on feature similarity.

    Args:
        keeper_df (pd.DataFrame): Original keeper dataframe with names and features.
        X_keeper_scaled (np.ndarray): Scaled feature matrix for keepers.
        target_name (str): Name of the keeper to find similar players to.
        top_n (int): Number of similar players to return.

    Returns:
        pd.DataFrame: Top N similar players (name + similarity score).
    """
    # Find index of the target player
    if target_name not in keeper_df["short_name"].values:
        raise ValueError(f"{target_name} not found in dataset.")

    target_idx = keeper_df[keeper_df["short_name"] == target_name].index[0]
    target_vector = X_keeper_scaled[target_idx].reshape(1, -1)

    # Calculate cosine similarity
    similarities = cosine_similarity(target_vector, X_keeper_scaled)[0]

    # Get top N most similar (excluding the player themselves)
    top_indices = similarities.argsort()[::-1]
    top_indices = [i for i in top_indices if i != target_idx][:top_n]

    similar_players = keeper_df.iloc[top_indices][["short_name"]].copy()
    similar_players["similarity"] = similarities[top_indices]

    return similar_players