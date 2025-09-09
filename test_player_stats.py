#!/usr/bin/env python3
"""
Test script for spillerstatistikk - analyserer kun noen få kamper for rask testing
"""

import pandas as pd
import numpy as np
from statsbombpy import sb
import warnings
warnings.filterwarnings('ignore')

def test_player_stats_with_few_matches():
    """Test spillerstatistikk med bare noen få kamper"""
    print("🧪 TESTING SPILLERSTATISTIKK MED FÅ KAMPER")
    print("="*50)
    
    # Premier League 2015/2016
    competition_id = 2
    season_id = 27
    
    # Hent kampliste
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    print(f"Totalt {len(matches)} kamper tilgjengelig")
    
    # Velg bare første 5 kamper for testing
    test_matches = matches.head(5)
    print(f"Tester med {len(test_matches)} kamper:")
    
    for _, match in test_matches.iterrows():
        print(f"  - {match['home_team']} vs {match['away_team']} ({match['match_date']})")
    
    # Hent events for disse kampene
    all_events = []
    
    for _, match in test_matches.iterrows():
        match_id = match['match_id']
        print(f"\nHenter events for kamp {match_id}...")
        
        try:
            events = sb.events(match_id=match_id)
            events['match_id'] = match_id
            events['home_team'] = match['home_team']
            events['away_team'] = match['away_team']
            all_events.append(events)
            print(f"  ✓ Hentet {len(events)} events")
        except Exception as e:
            print(f"  ❌ Feil: {e}")
    
    if not all_events:
        print("❌ Ingen events hentet")
        return
    
    # Kombiner alle events
    combined_events = pd.concat(all_events, ignore_index=True)
    print(f"\n✓ Totalt {len(combined_events):,} events fra {len(all_events)} kamper")
    
    # Analyser spillerstatistikk (forenklet versjon)
    player_events = combined_events[combined_events['player'].notna()].copy()
    print(f"Events med spillerinformasjon: {len(player_events):,}")
    
    # Grunnleggende statistikk per spiller
    player_stats = {}
    
    for _, event in player_events.iterrows():
        player = event['player']
        team = event['team']
        event_type = event['type']
        
        if player not in player_stats:
            player_stats[player] = {
                'player_name': player,
                'team': team,
                'total_events': 0,
                'passes': 0,
                'shots': 0,
                'goals': 0,
                'dribbles': 0,
                'tackles': 0,
                'interceptions': 0,
            }
        
        player_stats[player]['total_events'] += 1
        
        if event_type == 'Pass':
            player_stats[player]['passes'] += 1
        elif event_type == 'Shot':
            player_stats[player]['shots'] += 1
            if event.get('shot_outcome') == 'Goal':
                player_stats[player]['goals'] += 1
        elif event_type == 'Dribble':
            player_stats[player]['dribbles'] += 1
        elif event_type == 'Duel' and event.get('duel_type') == 'Tackle':
            player_stats[player]['tackles'] += 1
        elif event_type == 'Interception':
            player_stats[player]['interceptions'] += 1
    
    # Konverter til DataFrame
    stats_df = pd.DataFrame(list(player_stats.values()))
    stats_df = stats_df.sort_values('total_events', ascending=False)
    
    print(f"\n📊 RESULTATER:")
    print(f"Antall spillere analysert: {len(stats_df)}")
    
    print(f"\nTOP 10 SPILLERE (etter totale events):")
    top_players = stats_df.head(10)
    for _, player in top_players.iterrows():
        print(f"  {player['player_name']} ({player['team']}): {player['total_events']} events, "
              f"{player['passes']} pasninger, {player['shots']} skudd, {player['goals']} mål")
    
    # Lagre testresultater
    test_filename = "data/test_player_stats.csv"
    stats_df.to_csv(test_filename, index=False)
    print(f"\n✓ Testresultater lagret i: {test_filename}")
    
    print(f"\n💡 Hvis dette ser bra ut, kjør 'python3 generate_player_stats.py' for full analyse!")
    
    return stats_df

if __name__ == "__main__":
    test_player_stats_with_few_matches()
