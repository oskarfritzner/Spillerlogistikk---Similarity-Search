# Player Similarity Search

A Python tool that finds similar football players based on their playing style and position using statistical similarity metrics.

## What does it do?

This project analyzes football player statistics and finds players with similar characteristics. It uses weighted feature comparison and cosine similarity to match players based on their role (e.g., striker, midfielder, goalkeeper).

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the example

```bash
python3 main.py
```

This will search for players similar to Kevin De Bruyne (attacking midfielder) and Manuel Neuer (goalkeeper).

## How to use

```python
from search_functions.unified_search import search_players

# Find similar outfield players
results = search_players("K. De Bruyne", "cam", top_n=5)
print(results)

# Find similar goalkeepers
results = search_players("M. Neuer", "gk", top_n=5)
print(results)
```

### Supported Roles

- **Attackers**: `st` (striker), `cf` (center forward), `lw`/`rw` (wingers)
- **Midfielders**: `cam` (attacking mid), `cm` (center mid), `cdm` (defensive mid)
- **Defenders**: `cb` (center back), `lb`/`rb` (fullbacks), `rwb`/`lwb` (wingbacks)
- **Goalkeeper**: `gk`

## Project Structure

```
├── main.py                    # Example usage
├── data/                      # Player datasets (CSV files)
├── search_functions/          # Core search algorithms
│   ├── unified_search.py      # Main search interface
│   ├── op_similarity_search.py # Outfield player search
│   ├── gk_similarity_search.py # Goalkeeper search
│   └── role_profiles.py       # Position-specific feature weights
├── statsbomb/                 # StatsBomb data fetching scripts
└── advanced_similarity/       # Advanced analysis tools
```

## How it works

1. **Role Profiles**: Each position has weighted features (e.g., strikers prioritize shooting)
2. **Feature Scaling**: Player statistics are normalized using StandardScaler for fair comparison
3. **Similarity Calculation**: Uses cosine similarity and Euclidean distance to find similar players
4. **Ranking**: Returns the most similar players based on their statistical profiles

## Data Sources

- FIFA 22 player dataset (`players_22.csv`)
- StatsBomb open data for Premier League 2015/2016 season

---

For more detailed information about the StatsBomb data collection, see `SPILLERSTATISTIKK_README.md`.
