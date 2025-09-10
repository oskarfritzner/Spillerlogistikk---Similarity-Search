#!/usr/bin/env python3
"""
Enkelt eksempel på hvordan man henter data for Premier League 2015/2016
Dette er en forenklet versjon for rask testing og læring.
"""

from statsbombpy import sb
import pandas as pd

def main():
    print("Henter Premier League 2015/2016 data...")
    
    # Premier League 2015/2016
    competition_id = 2
    season_id = 27
    
    # Hent alle kamper
    print("1. Henter kampliste...")
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    print(f"   Fant {len(matches)} kamper")
    
    # Vis noen eksempler
    print("\nEksempler på kamper:")
    print(matches[['match_date', 'home_team', 'away_team', 'home_score', 'away_score']].head())
    
    # Hent events for første kamp som eksempel
    print(f"\n2. Henter events for første kamp...")
    first_match = matches.iloc[0]
    match_id = first_match['match_id']
    
    print(f"   Kamp: {first_match['home_team']} vs {first_match['away_team']}")
    print(f"   Dato: {first_match['match_date']}")
    
    events = sb.events(match_id=match_id)
    print(f"   Hentet {len(events)} events")
    
    # Vis event-typer
    print(f"\nEvent-typer i denne kampen:")
    print(events['type'].value_counts().head(10))
    
    # Lagre som eksempel
    matches.to_csv('data/matches_example.csv', index=False)
    events.to_csv('data/events_example.csv', index=False)
    
    print(f"\nEksempeldata lagret i:")
    print(f"- data/matches_example.csv ({len(matches)} kamper)")
    print(f"- data/events_example.csv ({len(events)} events fra én kamp)")
    
    print(f"\nFor å hente ALL data, kjør: python3 fetch_all_pl_2015_2016_data.py")

if __name__ == "__main__":
    main()
