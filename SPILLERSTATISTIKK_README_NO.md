# Premier League 2015/2016 Spillerstatistikk

Dette prosjektet inneholder script for å hente og analysere spillerstatistikk fra Premier League sesongen 2015/2016 ved hjelp av StatsBomb sitt åpne datasett.

## 📋 Oversikt

### Script tilgjengelig:

1. **`generate_player_stats.py`** - Hovedscript som henter alle data og genererer omfattende spillerstatistikk
2. **`test_player_stats.py`** - Testscript som analyserer bare noen få kamper for rask testing
3. **`fetch_all_pl_2015_2016_data.py`** - Henter all rådata (events) fra alle kamper
4. **`quick_fetch_example.py`** - Enkelt eksempel for å teste API-tilgang

## 🚀 Hvordan bruke

### 1. Installér avhengigheter

```bash
pip install -r requirements.txt
```

### 2. Test at alt fungerer

```bash
python3 test_player_stats.py
```

Dette analyserer bare 5 kamper og tar ~2 minutter.

### 3. Generer full spillerstatistikk (SMART versjon)

```bash
python3 generate_player_stats.py
```

🧠 **Smart funksjon**: Scriptet vil først søke etter eksisterende eventdata og tilby å bruke dem (sparer 20-30 minutter!). Hvis ingen finnes, henter det ny data fra API.

### 🚀 Anbefalt arbeidsflyt:

```bash
# Steg 1: Hent rådata først (gjør dette én gang, 20-30 min)
python3 fetch_all_pl_2015_2016_data.py

# Steg 2: Generer spillerstatistikk (bruker eksisterende data, 2-3 min!)
python3 generate_player_stats.py
```

**Resultat**: Total tid redusert fra 40-60 minutter til 20-35 minutter! 🎉

## 📊 Hva får du?

### Utdatafiler:

- `pl_2015_2016_player_stats_full_[timestamp].csv` - Komplett statistikk med alle detaljer
- `pl_2015_2016_player_stats_simple_[timestamp].csv` - Forenklet oversikt med hovedstatistikk
- `pl_2015_2016_top_scorers_[timestamp].csv` - Top 20 målscorere

### Statistikker inkludert:

#### ⚽ Angrepsstatistikk

- Mål scoret
- Skudd (totalt, på mål, utenfor, blokkert)
- Expected Goals (xG)
- Assists og nøkkelpasninger
- Hodestøt

#### 🎯 Pasningsstatistikk

- Pasninger forsøkt/fullført
- Pasningsprosent
- Korte/mellom/lange pasninger
- Fremover/bakover/sideveis pasninger
- Innlegg

#### 🏃‍♂️ Driblingsstatistikk

- Driblinger forsøkt/fullført
- Driblingsprosentprosent

#### 🛡️ Forsvarstatistikk

- Taklinger forsøkt/vunnet
- Avskjæringer (interceptions)
- Klaringer
- Blokkeringer
- Pressing

#### 🟨 Disiplin

- Foul begått/vunnet
- Gule kort
- Røde kort

#### 📍 Posisjonsdata

- Gjennomsnittlig posisjon (x,y koordinater)
- Ballkontakter
- Balltap

#### 📈 Per-kamp statistikk

- Pasninger per kamp
- Skudd per kamp
- Mål per kamp
- Assists per kamp

## 🎓 Pedagogisk forklaring

### Problemet:

Fotballanalyse krever detaljerte spillerstatistikker for å forstå prestasjoner og sammenligne spillere.

### Løsningen:

1. **Datainnhenting**: Bruker StatsBomb API for å hente event-data
2. **Aggregering**: Konverterer rå events til meningsfulle statistikker
3. **Kategorisering**: Organiserer statistikker i logiske grupper
4. **Normalisering**: Beregner per-kamp og prosentuelle mål

### Relevans for CIT4620:

- **Feature Engineering**: Konvertering av rå data til ML-features
- **Data Preprocessing**: Rensing og strukturering av store datasett
- **Statistical Analysis**: Beregning av avledede mål og sammendrag
- **Big Data**: Håndtering av ~760,000 events fra 380 kamper

## 🔍 Eksempel på bruk

```python
import pandas as pd

# Last inn spillerstatistikk
stats = pd.read_csv('data/pl_2015_2016_player_stats_simple_[timestamp].csv')

# Finn toppscorere
top_scorers = stats.nlargest(10, 'goals_scored')
print(top_scorers[['player_name', 'team', 'goals_scored', 'assists']])

# Spillere med best pasningsprosent (min 1000 pasninger)
accurate_passers = stats[stats['passes_attempted'] >= 1000]
best_passers = accurate_passers.nlargest(10, 'pass_completion_rate')

# Mest kreative spillere
creative = stats.nlargest(10, 'key_passes')
```

## 📈 Eksempel på resultater

### Toppscorere (forventet):

1. **Harry Kane** - Tottenham
2. **Sergio Agüero** - Manchester City
3. **Jamie Vardy** - Leicester City (mesterskapssesongen!)
4. **Romelu Lukaku** - Everton
5. **Olivier Giroud** - Arsenal

### Beste pasningsprosent:

- Sentrale forsvarere og defensive midtbanespillere
- Keepere (korte pasninger)

### Mest kreative spillere:

- Offensive midtbanespillere
- Kantspillere med mange innlegg

## 🚨 Tips og advarsler

### Performance:

- Full analyse tar lang tid - vær tålmodig!
- Test først med `test_player_stats.py`
- Scriptene bruker API rate limiting for å unngå blokkering

### Datakvalitet:

- StatsBomb data er svært detaljert og nøyaktig
- Noen kamper kan mangle visse event-typer
- Posisjondata er i StatsBomb sitt koordinatsystem (120x80)

### Filstørrelser:

- Full statistikk: ~2-5 MB
- Rådata (hvis hentet): ~200-500 MB

## 🔧 Feilsøking

### Vanlige problemer:

1. **Import error**: Installer `statsbombpy` med `pip install statsbombpy`
2. **API timeout**: Prøv igjen senere, eller øk pause-tiden i scriptet
3. **Manglende data**: Noen kamper kan ha begrenset data tilgjengelig

### Debug:

```bash
python3 -c "import statsbombpy; print('StatsBomb OK')"
python3 quick_fetch_example.py  # Test API-tilgang
```

## 📚 Videre utvikling

### Mulige utvidelser:

- Heatmaps basert på posisjonsdata
- Spillersammenligning og clustering
- Prediktive modeller for spillerprestasjon
- Integrasjon med andre sesonger/ligaer

### For CIT4620 prosjekter:

- Bruk statistikken som features for ML-modeller
- Implementer similarity search basert på spillerstiler
- Lag neural networks for spillerprestasjon prediksjon

---

**Laget av AI Assistant for CIT4620 - Evolutionary AI and Robotics**  
_OsloMet - September 2025_
