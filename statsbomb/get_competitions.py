from statsbombpy import sb
import pandas as pd

# Get all available competitions
comps = sb.competitions()

# Show all competitions (including IDs)
print(comps[['competition_id', 'season_id', 'competition_name', 'season_name']])

# Step 2: Save to CSV
comps.to_csv("data/competitions.csv", index=False)

print("✅ competitions.csv saved successfully!")