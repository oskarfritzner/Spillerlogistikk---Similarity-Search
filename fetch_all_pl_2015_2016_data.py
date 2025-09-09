#!/usr/bin/env python3
"""
Script for å hente ut all data per kamp for Premier League sesongen 2015/2016
Dette scriptet bruker StatsBomb sitt åpne datasett via statsbombpy biblioteket.

Forfatter: AI Assistant
Dato: September 2025
"""

import pandas as pd
from statsbombpy import sb
import os
import time
from datetime import datetime


def create_data_directory():
    """Opprett data-mappe hvis den ikke eksisterer"""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Opprettet 'data' mappe")


def fetch_premier_league_matches():
    """
    Hent alle kamper fra Premier League 2015/2016 sesongen
    
    Returns:
        pd.DataFrame: DataFrame med alle kamper
    """
    print("Henter kampliste for Premier League 2015/2016...")
    
    # Premier League 2015/2016 ID-er
    competition_id = 2
    season_id = 27
    
    try:
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        print(f"✓ Hentet {len(matches)} kamper")
        return matches
    except Exception as e:
        print(f"❌ Feil ved henting av kamper: {e}")
        return None


def fetch_match_events(match_id, match_info):
    """
    Hent alle events for en spesifikk kamp
    
    Args:
        match_id (int): Kamp ID
        match_info (dict): Informasjon om kampen
        
    Returns:
        pd.DataFrame: DataFrame med alle events for kampen
    """
    try:
        events = sb.events(match_id=match_id)
        
        # Legg til kampinformasjon i events dataframe
        events['match_id'] = match_id
        events['home_team'] = match_info['home_team']
        events['away_team'] = match_info['away_team']
        events['match_date'] = match_info['match_date']
        events['home_score'] = match_info['home_score']
        events['away_score'] = match_info['away_score']
        
        return events
        
    except Exception as e:
        print(f"   ❌ Feil ved henting av events for kamp {match_id}: {e}")
        return None


def fetch_all_match_data(matches_df):
    """
    Hent events for alle kamper og kombiner til én stor dataset
    
    Args:
        matches_df (pd.DataFrame): DataFrame med alle kamper
        
    Returns:
        pd.DataFrame: Kombinert DataFrame med alle events fra alle kamper
    """
    all_events = []
    total_matches = len(matches_df)
    
    print(f"\nHenter eventdata for {total_matches} kamper...")
    print("Dette kan ta litt tid...")
    
    for idx, (_, match) in enumerate(matches_df.iterrows(), 1):
        match_id = match['match_id']
        
        print(f"({idx}/{total_matches}) Henter data for: {match['home_team']} vs {match['away_team']} - {match['match_date']}")
        
        # Hent events for denne kampen
        events = fetch_match_events(match_id, match)
        
        if events is not None:
            all_events.append(events)
            print(f"   ✓ Hentet {len(events)} events")
        
        # Liten pause for å unngå å overbelaste API-et
        time.sleep(0.5)
    
    if all_events:
        # Kombiner alle events til én DataFrame
        combined_events = pd.concat(all_events, ignore_index=True)
        print(f"\n✓ Totalt hentet {len(combined_events)} events fra {len(all_events)} kamper")
        return combined_events
    else:
        print("❌ Ingen events ble hentet")
        return None


def save_data(matches_df, all_events_df):
    """
    Lagre data til CSV-filer
    
    Args:
        matches_df (pd.DataFrame): DataFrame med kamper
        all_events_df (pd.DataFrame): DataFrame med alle events
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Lagre kamper
    matches_filename = f"data/pl_2015_2016_matches_{timestamp}.csv"
    matches_df.to_csv(matches_filename, index=False)
    print(f"✓ Kamper lagret i: {matches_filename}")
    
    # Lagre alle events
    if all_events_df is not None:
        events_filename = f"data/pl_2015_2016_all_events_{timestamp}.csv"
        all_events_df.to_csv(events_filename, index=False)
        print(f"✓ Alle events lagret i: {events_filename}")
        
        # Lag også en komprimert versjon
        events_compressed = f"data/pl_2015_2016_all_events_{timestamp}.csv.gz"
        all_events_df.to_csv(events_compressed, index=False, compression='gzip')
        print(f"✓ Komprimert versjon lagret i: {events_compressed}")
        
        return matches_filename, events_filename, events_compressed
    
    return matches_filename, None, None


def print_data_summary(matches_df, all_events_df):
    """
    Skriv ut sammendrag av dataene som ble hentet
    
    Args:
        matches_df (pd.DataFrame): DataFrame med kamper
        all_events_df (pd.DataFrame): DataFrame med alle events
    """
    print("\n" + "="*60)
    print("SAMMENDRAG AV HENTET DATA")
    print("="*60)
    
    print(f"Antall kamper: {len(matches_df)}")
    print(f"Periode: {matches_df['match_date'].min()} til {matches_df['match_date'].max()}")
    
    if all_events_df is not None:
        print(f"Totalt antall events: {len(all_events_df):,}")
        print(f"Antall unike lag: {len(set(all_events_df['home_team'].unique()) | set(all_events_df['away_team'].unique()))}")
        print(f"Event typer: {', '.join(all_events_df['type'].value_counts().head(10).index.tolist())}")
        
        # Filstørrelse estimat
        events_size_mb = all_events_df.memory_usage(deep=True).sum() / (1024 * 1024)
        print(f"Estimert filstørrelse: {events_size_mb:.1f} MB")
    
    print("="*60)


def main():
    """Hovedfunksjon som kjører hele prosessen"""
    print("🏈 PREMIER LEAGUE 2015/2016 DATA HENTER")
    print("="*50)
    
    # Opprett data-mappe
    create_data_directory()
    
    # Hent kampliste
    matches_df = fetch_premier_league_matches()
    if matches_df is None:
        print("❌ Kunne ikke hente kampliste. Avbryter.")
        return
    
    # Spør bruker om de vil hente alle events
    print(f"\nFant {len(matches_df)} kamper.")
    user_input = input("Vil du hente eventdata for alle kamper? Dette kan ta 10-20 minutter (y/n): ").lower().strip()
    
    if user_input in ['y', 'yes', 'ja', 'j']:
        # Hent alle events
        all_events_df = fetch_all_match_data(matches_df)
    else:
        print("Hopper over henting av eventdata.")
        all_events_df = None
    
    # Lagre data
    files_created = save_data(matches_df, all_events_df)
    
    # Skriv ut sammendrag
    print_data_summary(matches_df, all_events_df)
    
    print("\n✅ Ferdig! Data er lagret i 'data' mappen.")
    
    if all_events_df is not None:
        print("\n💡 Tips:")
        print("- Bruk den komprimerte (.gz) filen for lagring")
        print("- Bruk den vanlige CSV-filen for analyse")
        print("- Dataene inneholder detaljert informasjon om hver hendelse i kampene")


if __name__ == "__main__":
    main()
