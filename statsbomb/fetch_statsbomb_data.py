from statsbombpy import sb
import pandas as pd

# Get available competitions
comps = sb.competitions()

# Pick a competition & season
matches = sb.matches(competition_id=55, season_id=282)  # Euro 2024

# Pick a match
match_id = matches.iloc[0].match_id

# Get all events from the match
events = sb.events(match_id=match_id)
print(events.head())