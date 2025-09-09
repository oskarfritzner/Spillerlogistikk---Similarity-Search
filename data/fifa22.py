import pandas as pd
from sklearn.preprocessing import StandardScaler

# === 1. Load dataset ===
# Read the FIFA 22 player dataset from CSV
dataset = pd.read_csv("data/players_22.csv")

# -------------------------------------------
# === 2. Define feature sets for each player type ===

# For outfield players (not goalkeepers)
outfield_features = [
    'age', 'height_cm', 'weight_kg',
    'overall', 'potential', 'value_eur',
    'pace', 'shooting', 'passing',
    'dribbling', 'defending', 'physic'
]

# For goalkeepers
keeper_features = [
    'age', 'height_cm', 'weight_kg',
    'overall', 'potential', 'value_eur',
    'goalkeeping_diving', 'goalkeeping_handling',
    'goalkeeping_kicking', 'goalkeeping_positioning',
    'goalkeeping_reflexes'
]

# -------------------------------------------
# === 3. Clean and filter outfield player data ===

# Step 1: Remove goalkeepers from dataset
outfield_df = dataset[~dataset['player_positions'].str.contains('GK', na=False)]

# Step 2: Keep only relevant features + player name
outfield_df = outfield_df[outfield_features + ["short_name"]]

# Step 3: Drop rows with missing values (NaNs) – to ensure clean data
outfield_df = outfield_df.dropna()

# -------------------------------------------
# === 4. Clean and filter goalkeeper data ===

# Step 1: Select only goalkeepers
keeper_df = dataset[dataset['player_positions'].str.contains('GK', na=False)]

# Step 2: Keep only relevant keeper features + player name
keeper_df = keeper_df[keeper_features + ["short_name"]]

# Step 3: Drop rows with missing values
keeper_df = keeper_df.dropna()

# -------------------------------------------
# === 5. Normalize the data ===

# Initialize a standard scaler (z-score normalization)
scaler = StandardScaler()

# Fit and transform the outfield player features into standardized form
# All features will now have mean = 0 and std = 1
X_outfield = scaler.fit_transform(outfield_df[outfield_features])

# Same process for goalkeepers
X_keeper = scaler.fit_transform(keeper_df[keeper_features])

# -------------------------------------------
# === 6. Preview cleaned data and stats ===

# Print the first 10 keepers after cleaning
print(keeper_df.head(10))

# Show how many goalkeepers made it through the cleaning step
print(f"Number of goalkeepers after cleaning: {len(keeper_df)}")