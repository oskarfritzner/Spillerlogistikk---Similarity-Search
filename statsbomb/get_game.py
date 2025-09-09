from statsbombpy import sb

# Hent alle kamper i PL 2024/25
matches = sb.matches(competition_id=2, season_id=2024)

# Vis første kamp
print(matches[['match_id', 'home_team', 'away_team', 'match_date']].head())

# Velg en kamp
match_id = matches.iloc[0]['match_id']  # eller velg spesifikk kamp hvis du vil

# Hent eventdata for kampen
events_df = sb.events(match_id=match_id)

# Sjekk kolonnene (statstyper)
print(events_df.columns)

# Vis de første radene
print(events_df.head())