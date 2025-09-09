from statsbombpy import sb
import pandas as pd

# Premier League 2015/2016
competition_id = 2
season_id = 27

# Hent alle kamper
matches = sb.matches(competition_id=competition_id, season_id=season_id)
matches.to_csv("data/premier_league_2015_2016_matches.csv", index=False)
print(f"{len(matches)} kamper lagret i premier_league_2015_2016_matches.csv")

# Velg én kamp for å inspisere events
match_id = matches.iloc[0]["match_id"]
print("Henter eventdata for kamp:", match_id)

events = sb.events(match_id=match_id)
events.to_csv("data/sample_match_events.csv", index=False)
print(f"{len(events)} events lagret i sample_match_events.csv")