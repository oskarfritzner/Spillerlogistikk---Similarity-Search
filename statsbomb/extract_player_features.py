# extract_player_features.py

from statsbombpy import sb
import pandas as pd

# Velg kamp (du kan bla i sb.competitions() og sb.matches() for å finne IDer)
match_id = 3943043  # Euros 2024-finalen f.eks.

# Hent events fra match
events = sb.events(match_id=match_id)

# Filtrer for pasninger, skudd, taklinger osv.
passes = events[events['type'] == 'Pass']
shots = events[events['type'] == 'Shot']
tackles = events[events['type'] == 'Pressure']

# Eksempel: Antall pasninger per spiller
pass_counts = passes.groupby('player')['id'].count().reset_index()
pass_counts.columns = ['player', 'num_passes']

# Antall skudd
shot_counts = shots.groupby('player')['id'].count().reset_index()
shot_counts.columns = ['player', 'num_shots']

# Samle alt i én dataframe
player_stats = pd.merge(pass_counts, shot_counts, on='player', how='outer')
player_stats.fillna(0, inplace=True)

# Eksporter til CSV
player_stats.to_csv("data/player_features.csv", index=False)
print("✅ Saved player_features.csv")