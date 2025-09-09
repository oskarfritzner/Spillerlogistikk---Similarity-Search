# unified_search.py

import pandas as pd
from sklearn.preprocessing import StandardScaler

from search_functions.role_profiles import role_profiles
from search_functions.op_similarity_search import find_similar_outfield_players
from search_functions.gk_similarity_search import find_similar_goalkeepers


def search_players(player_name: str, player_role: str, top_n: int = 10):
    """
    Unified search function for both outfield players and goalkeepers.
    """
    # Load dataset
    dataset = pd.read_csv("data/players_22.csv", low_memory=False)

    # Check if role is known
    if player_role not in role_profiles:
        raise ValueError(f"Unknown role: '{player_role}'")

    profile = role_profiles[player_role]

    if player_role == "gk":
        keeper_features = [
            'age', 'height_cm', 'weight_kg',
            'overall', 'potential', 'value_eur',
            'goalkeeping_diving', 'goalkeeping_handling',
            'goalkeeping_kicking', 'goalkeeping_positioning',
            'goalkeeping_reflexes'
        ]

        keeper_df = dataset[dataset['player_positions'].str.contains('GK', na=False)]
        keeper_df = keeper_df[keeper_features + ["short_name"]].dropna()

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(keeper_df[keeper_features])

        return find_similar_goalkeepers(
            keeper_df=keeper_df,
            X_keeper_scaled=X_scaled,
            target_name=player_name,
            top_n=top_n
        )

    else:
        outfield_features = [
            'age', 'height_cm', 'weight_kg',
            'overall', 'potential', 'value_eur',
            'pace', 'shooting', 'passing',
            'dribbling', 'defending', 'physic'
        ]

        outfield_df = dataset[~dataset['player_positions'].str.contains('GK', na=False)]
        outfield_df = outfield_df[outfield_features + ['short_name']].dropna()

        return find_similar_outfield_players(
            player_name=player_name,
            dataset=outfield_df,
            feature_list=list(profile.keys()),
            weights_dict=profile,
            top_n=top_n
        )