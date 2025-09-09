#!/usr/bin/env python3
"""
Script for å generere omfattende spillerstatistikk for Premier League 2015/2016
Dette scriptet henter eventdata fra alle kamper og aggregerer statistikker per spiller.

Forfatter: AI Assistant
Dato: September 2025
"""

import pandas as pd
import numpy as np
from statsbombpy import sb
import os
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def create_data_directory():
    """Opprett data-mappe hvis den ikke eksisterer"""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Opprettet 'data' mappe")


def fetch_all_events_for_season():
    """
    Hent alle events for alle kamper i Premier League 2015/2016
    
    Returns:
        pd.DataFrame: Kombinert DataFrame med alle events
    """
    print("Henter alle events for Premier League 2015/2016...")
    
    # Premier League 2015/2016
    competition_id = 2
    season_id = 27
    
    try:
        # Hent alle kamper
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        print(f"Fant {len(matches)} kamper")
        
        all_events = []
        total_matches = len(matches)
        
        print("Henter eventdata for alle kamper...")
        
        for idx, (_, match) in enumerate(matches.iterrows(), 1):
            match_id = match['match_id']
            
            if idx % 20 == 0:  # Progress update hver 20. kamp
                print(f"Behandler kamp {idx}/{total_matches}...")
            
            try:
                events = sb.events(match_id=match_id)
                
                # Legg til kampinformasjon
                events['match_id'] = match_id
                events['home_team'] = match['home_team']
                events['away_team'] = match['away_team']
                events['match_date'] = match['match_date']
                events['home_score'] = match['home_score']
                events['away_score'] = match['away_score']
                events['match_week'] = match['match_week']
                
                all_events.append(events)
                
                # Liten pause for å unngå å overbelaste API-et
                time.sleep(0.3)
                
            except Exception as e:
                print(f"   Feil ved henting av kamp {match_id}: {e}")
                continue
        
        if all_events:
            combined_events = pd.concat(all_events, ignore_index=True)
            print(f"✓ Totalt hentet {len(combined_events):,} events")
            return combined_events
        else:
            print("❌ Ingen events ble hentet")
            return None
            
    except Exception as e:
        print(f"❌ Feil ved henting av data: {e}")
        return None


def calculate_player_statistics(events_df):
    """
    Beregn omfattende spillerstatistikk fra eventdata
    
    Args:
        events_df (pd.DataFrame): DataFrame med alle events
        
    Returns:
        pd.DataFrame: DataFrame med spillerstatistikk
    """
    print("Beregner spillerstatistikk...")
    
    # Filtrer ut rader uten spillerinformasjon
    player_events = events_df[events_df['player'].notna()].copy()
    
    print(f"Behandler {len(player_events):,} events med spillerinformasjon")
    
    # Opprett tom statistikk-dict
    player_stats = {}
    
    # Grunnleggende spillerinformasjon
    for _, event in player_events.iterrows():
        player_name = event['player']
        player_id = event.get('player_id', 'unknown')
        team = event['team']
        
        if player_name not in player_stats:
            player_stats[player_name] = {
                'player_name': player_name,
                'player_id': player_id,
                'team': team,
                'matches_played': set(),
                
                # Grunnleggende statistikk
                'total_events': 0,
                'minutes_played': 0,
                
                # Pasningsstatistikk
                'passes_attempted': 0,
                'passes_completed': 0,
                'passes_failed': 0,
                'pass_completion_rate': 0,
                'short_passes': 0,
                'medium_passes': 0,
                'long_passes': 0,
                'forward_passes': 0,
                'backward_passes': 0,
                'sideways_passes': 0,
                'key_passes': 0,
                'assists': 0,
                'crosses_attempted': 0,
                'crosses_completed': 0,
                
                # Skuddstatistikk
                'shots_total': 0,
                'shots_on_target': 0,
                'shots_off_target': 0,
                'shots_blocked': 0,
                'goals_scored': 0,
                'shots_from_inside_box': 0,
                'shots_from_outside_box': 0,
                'headers': 0,
                'total_xg': 0,
                
                # Driblingstatistikk
                'dribbles_attempted': 0,
                'dribbles_completed': 0,
                'dribbles_failed': 0,
                'dribble_success_rate': 0,
                
                # Forsvarsspill
                'tackles_attempted': 0,
                'tackles_won': 0,
                'interceptions': 0,
                'clearances': 0,
                'blocks': 0,
                'pressure_events': 0,
                'fouls_committed': 0,
                'fouls_won': 0,
                'yellow_cards': 0,
                'red_cards': 0,
                
                # Keeperstatistikk (hvis relevant)
                'saves': 0,
                'goals_conceded': 0,
                'clean_sheets': 0,
                
                # Posisjonsdata
                'avg_position_x': [],
                'avg_position_y': [],
                'distance_covered': 0,
                
                # Ballkontakt
                'ball_receipts': 0,
                'ball_recoveries': 0,
                'dispossessed': 0,
                'miscontrols': 0,
            }
        
        # Legg til kamp til spillerens kampliste
        player_stats[player_name]['matches_played'].add(event['match_id'])
        player_stats[player_name]['total_events'] += 1
        
        # Behandle forskjellige event-typer
        event_type = event['type']
        
        # Posisjondata
        if pd.notna(event.get('location')):
            try:
                if isinstance(event['location'], list) and len(event['location']) >= 2:
                    x, y = event['location'][0], event['location'][1]
                    player_stats[player_name]['avg_position_x'].append(x)
                    player_stats[player_name]['avg_position_y'].append(y)
            except:
                pass
        
        # PASNINGER
        if event_type == 'Pass':
            player_stats[player_name]['passes_attempted'] += 1
            
            # Pasning resultat
            if pd.isna(event.get('pass_outcome')):  # Vellykket pasning
                player_stats[player_name]['passes_completed'] += 1
            else:
                player_stats[player_name]['passes_failed'] += 1
            
            # Pasningslengde
            pass_length = event.get('pass_length', 0)
            if pass_length < 15:
                player_stats[player_name]['short_passes'] += 1
            elif pass_length < 30:
                player_stats[player_name]['medium_passes'] += 1
            else:
                player_stats[player_name]['long_passes'] += 1
            
            # Pasningsretning (basert på vinkel)
            pass_angle = event.get('pass_angle', 0)
            if pass_angle is not None:
                if -0.5 < pass_angle < 0.5:  # Fremover
                    player_stats[player_name]['forward_passes'] += 1
                elif abs(pass_angle) > 2.6:  # Bakover
                    player_stats[player_name]['backward_passes'] += 1
                else:  # Sideveis
                    player_stats[player_name]['sideways_passes'] += 1
            
            # Spesielle pasninger
            if event.get('pass_shot_assist') == True:
                player_stats[player_name]['assists'] += 1
                
            if event.get('pass_key_pass_id') is not None:
                player_stats[player_name]['key_passes'] += 1
                
            if event.get('pass_cross') == True:
                player_stats[player_name]['crosses_attempted'] += 1
                if pd.isna(event.get('pass_outcome')):
                    player_stats[player_name]['crosses_completed'] += 1
        
        # SKUDD
        elif event_type == 'Shot':
            player_stats[player_name]['shots_total'] += 1
            
            # xG (Expected Goals)
            xg_value = event.get('shot_statsbomb_xg', 0)
            if xg_value is not None:
                player_stats[player_name]['total_xg'] += xg_value
            
            # Skudd resultat
            shot_outcome = event.get('shot_outcome')
            if shot_outcome == 'Goal':
                player_stats[player_name]['goals_scored'] += 1
                player_stats[player_name]['shots_on_target'] += 1
            elif shot_outcome in ['Saved', 'Saved To Post']:
                player_stats[player_name]['shots_on_target'] += 1
            elif shot_outcome == 'Blocked':
                player_stats[player_name]['shots_blocked'] += 1
            else:
                player_stats[player_name]['shots_off_target'] += 1
            
            # Skuddposisjon
            if event.get('location'):
                try:
                    x_pos = event['location'][0]
                    if x_pos >= 102:  # I boksen (antar 120x80 bane)
                        player_stats[player_name]['shots_from_inside_box'] += 1
                    else:
                        player_stats[player_name]['shots_from_outside_box'] += 1
                except:
                    pass
            
            # Hodestøt
            if event.get('shot_body_part') == 'Head':
                player_stats[player_name]['headers'] += 1
        
        # DRIBLING
        elif event_type == 'Dribble':
            player_stats[player_name]['dribbles_attempted'] += 1
            
            if event.get('dribble_outcome') == 'Complete':
                player_stats[player_name]['dribbles_completed'] += 1
            else:
                player_stats[player_name]['dribbles_failed'] += 1
        
        # FORSVARSSPILL
        elif event_type == 'Duel':
            if event.get('duel_type') == 'Tackle':
                player_stats[player_name]['tackles_attempted'] += 1
                if event.get('duel_outcome') == 'Won':
                    player_stats[player_name]['tackles_won'] += 1
        
        elif event_type == 'Interception':
            player_stats[player_name]['interceptions'] += 1
            
        elif event_type == 'Clearance':
            player_stats[player_name]['clearances'] += 1
            
        elif event_type == 'Block':
            player_stats[player_name]['blocks'] += 1
            
        elif event_type == 'Pressure':
            player_stats[player_name]['pressure_events'] += 1
        
        # FOUL
        elif event_type == 'Foul Committed':
            player_stats[player_name]['fouls_committed'] += 1
            
            # Kort
            card = event.get('foul_committed_card')
            if card == 'Yellow Card':
                player_stats[player_name]['yellow_cards'] += 1
            elif card in ['Red Card', 'Second Yellow']:
                player_stats[player_name]['red_cards'] += 1
                
        elif event_type == 'Foul Won':
            player_stats[player_name]['fouls_won'] += 1
        
        # BALLKONTAKT
        elif event_type == 'Ball Receipt*':
            player_stats[player_name]['ball_receipts'] += 1
            
        elif event_type == 'Ball Recovery':
            player_stats[player_name]['ball_recoveries'] += 1
            
        elif event_type == 'Dispossessed':
            player_stats[player_name]['dispossessed'] += 1
            
        elif event_type == 'Miscontrol':
            player_stats[player_name]['miscontrols'] += 1
        
        # KEEPER
        elif event_type == 'Goal Keeper':
            goalkeeper_outcome = event.get('goalkeeper_outcome')
            if goalkeeper_outcome in ['Saved', 'Claim', 'Punch']:
                player_stats[player_name]['saves'] += 1
    
    # Beregn avledede statistikker
    final_stats = []
    
    for player_name, stats in player_stats.items():
        # Konverter set til count
        stats['matches_played'] = len(stats['matches_played'])
        
        # Beregn rater og gjennomsnitt
        if stats['passes_attempted'] > 0:
            stats['pass_completion_rate'] = (stats['passes_completed'] / stats['passes_attempted']) * 100
        
        if stats['dribbles_attempted'] > 0:
            stats['dribble_success_rate'] = (stats['dribbles_completed'] / stats['dribbles_attempted']) * 100
        
        if stats['shots_total'] > 0:
            stats['shot_accuracy'] = (stats['shots_on_target'] / stats['shots_total']) * 100
        else:
            stats['shot_accuracy'] = 0
        
        # Gjennomsnittlig posisjon
        if stats['avg_position_x']:
            stats['avg_position_x'] = np.mean(stats['avg_position_x'])
            stats['avg_position_y'] = np.mean(stats['avg_position_y'])
        else:
            stats['avg_position_x'] = 0
            stats['avg_position_y'] = 0
        
        # Per-kamp statistikk
        if stats['matches_played'] > 0:
            stats['passes_per_game'] = stats['passes_attempted'] / stats['matches_played']
            stats['shots_per_game'] = stats['shots_total'] / stats['matches_played']
            stats['goals_per_game'] = stats['goals_scored'] / stats['matches_played']
            stats['assists_per_game'] = stats['assists'] / stats['matches_played']
        else:
            stats['passes_per_game'] = 0
            stats['shots_per_game'] = 0
            stats['goals_per_game'] = 0
            stats['assists_per_game'] = 0
        
        final_stats.append(stats)
    
    # Konverter til DataFrame
    df = pd.DataFrame(final_stats)
    
    # Sorter etter antall kamper spilt og deretter total events
    df = df.sort_values(['matches_played', 'total_events'], ascending=[False, False])
    
    print(f"✓ Beregnet statistikk for {len(df)} spillere")
    
    return df


def save_player_statistics(stats_df):
    """
    Lagre spillerstatistikk til CSV-filer
    
    Args:
        stats_df (pd.DataFrame): DataFrame med spillerstatistikk
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Full statistikk
    full_filename = f"data/pl_2015_2016_player_stats_full_{timestamp}.csv"
    stats_df.to_csv(full_filename, index=False)
    print(f"✓ Full spillerstatistikk lagret i: {full_filename}")
    
    # Forenklet statistikk (kun hovedstatistikk)
    key_columns = [
        'player_name', 'team', 'matches_played', 'total_events',
        'passes_attempted', 'passes_completed', 'pass_completion_rate',
        'shots_total', 'shots_on_target', 'goals_scored', 'assists',
        'dribbles_attempted', 'dribbles_completed', 'dribble_success_rate',
        'tackles_attempted', 'tackles_won', 'interceptions', 'clearances',
        'fouls_committed', 'fouls_won', 'yellow_cards', 'red_cards',
        'total_xg', 'passes_per_game', 'shots_per_game', 'goals_per_game', 'assists_per_game'
    ]
    
    simple_stats = stats_df[key_columns].copy()
    simple_filename = f"data/pl_2015_2016_player_stats_simple_{timestamp}.csv"
    simple_stats.to_csv(simple_filename, index=False)
    print(f"✓ Forenklet spillerstatistikk lagret i: {simple_filename}")
    
    # Toppscorer oversikt
    top_scorers = stats_df.nlargest(20, 'goals_scored')[
        ['player_name', 'team', 'matches_played', 'goals_scored', 'assists', 'shots_total', 'total_xg']
    ]
    scorer_filename = f"data/pl_2015_2016_top_scorers_{timestamp}.csv"
    top_scorers.to_csv(scorer_filename, index=False)
    print(f"✓ Toppscorer oversikt lagret i: {scorer_filename}")
    
    return full_filename, simple_filename, scorer_filename


def print_statistics_summary(stats_df):
    """
    Skriv ut sammendrag av spillerstatistikken
    
    Args:
        stats_df (pd.DataFrame): DataFrame med spillerstatistikk
    """
    print("\n" + "="*70)
    print("SAMMENDRAG AV SPILLERSTATISTIKK - PREMIER LEAGUE 2015/2016")
    print("="*70)
    
    print(f"Totalt antall spillere: {len(stats_df)}")
    print(f"Spillere med minst 10 kamper: {len(stats_df[stats_df['matches_played'] >= 10])}")
    print(f"Spillere med minst 20 kamper: {len(stats_df[stats_df['matches_played'] >= 20])}")
    
    print(f"\nTOPPSCORER:")
    top_scorers = stats_df.nlargest(5, 'goals_scored')
    for _, player in top_scorers.iterrows():
        print(f"  {player['player_name']} ({player['team']}): {player['goals_scored']} mål")
    
    print(f"\nTOP ASSIST:")
    top_assists = stats_df.nlargest(5, 'assists')
    for _, player in top_assists.iterrows():
        print(f"  {player['player_name']} ({player['team']}): {player['assists']} assists")
    
    print(f"\nFLEST PASNINGER:")
    top_passers = stats_df.nlargest(5, 'passes_attempted')
    for _, player in top_passers.iterrows():
        print(f"  {player['player_name']} ({player['team']}): {player['passes_attempted']} pasninger")
    
    print(f"\nHØYEST PASNINGSPROSENT (min 500 pasninger):")
    accurate_passers = stats_df[stats_df['passes_attempted'] >= 500].nlargest(5, 'pass_completion_rate')
    for _, player in accurate_passers.iterrows():
        print(f"  {player['player_name']} ({player['team']}): {player['pass_completion_rate']:.1f}%")
    
    print("="*70)


def main():
    """Hovedfunksjon som kjører hele prosessen"""
    print("🏈 PREMIER LEAGUE 2015/2016 SPILLERSTATISTIKK GENERATOR")
    print("="*60)
    
    # Opprett data-mappe
    create_data_directory()
    
    # Spør bruker om de vil fortsette
    print("Dette scriptet vil hente eventdata for alle kamper og beregne spillerstatistikk.")
    print("Prosessen kan ta 20-30 minutter avhengig av internettforbindelse.")
    
    user_input = input("\nVil du fortsette? (y/n): ").lower().strip()
    
    if user_input not in ['y', 'yes', 'ja', 'j']:
        print("Avbryter.")
        return
    
    # Hent alle events
    print("\n1. HENTER EVENTDATA...")
    all_events = fetch_all_events_for_season()
    
    if all_events is None:
        print("❌ Kunne ikke hente eventdata. Avbryter.")
        return
    
    # Beregn spillerstatistikk
    print("\n2. BEREGNER SPILLERSTATISTIKK...")
    player_stats = calculate_player_statistics(all_events)
    
    if player_stats is None or len(player_stats) == 0:
        print("❌ Kunne ikke beregne spillerstatistikk. Avbryter.")
        return
    
    # Lagre statistikk
    print("\n3. LAGRER STATISTIKK...")
    files_created = save_player_statistics(player_stats)
    
    # Skriv ut sammendrag
    print_statistics_summary(player_stats)
    
    print(f"\n✅ Ferdig! Spillerstatistikk er lagret i 'data' mappen.")
    print(f"\nOpprettede filer:")
    for filename in files_created:
        print(f"  - {filename}")
    
    print(f"\n💡 Tips:")
    print(f"- Bruk '_simple' filen for grunnleggende analyse")
    print(f"- Bruk '_full' filen for detaljert analyse")
    print(f"- '_top_scorers' gir en rask oversikt over målscorere")


if __name__ == "__main__":
    main()
