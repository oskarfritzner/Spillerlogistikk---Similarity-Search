import pandas as pd
from sklearn.preprocessing import StandardScaler
from search_functions.gk_similarity_search import find_similar_goalkeepers

# Load data
dataset = pd.read_csv("data/players_22.csv")

# --- Clean and prepare keeper data ---
keeper_features = [
    'age', 'height_cm', 'weight_kg',
    'overall', 'potential', 'value_eur',
    'goalkeeping_diving', 'goalkeeping_handling',
    'goalkeeping_kicking', 'goalkeeping_positioning',
    'goalkeeping_reflexes'
]

keeper_df = dataset[dataset['player_positions'].str.contains('GK', na=False)]
keeper_df = keeper_df[keeper_features + ["short_name"]].dropna()

# --- Scale features ---
scaler = StandardScaler()
X_keeper_scaled = scaler.fit_transform(keeper_df[keeper_features])

# --- Run similarity search ---
target_name = "M. Neuer"
similar = find_similar_goalkeepers(keeper_df, X_keeper_scaled, target_name)

# --- Print results ---
print(f"Most similar goalkeepers to {target_name}:\n")
print(similar)