# Premier League 2015/2016 Player Statistics

This project contains scripts to fetch and analyze player statistics from the Premier League 2015/2016 season using StatsBomb's open dataset.

## 📋 Overview

### Available Scripts:

1. **`generate_player_stats.py`** - Main script that fetches all data and generates comprehensive player statistics
2. **`test_player_stats.py`** - Test script that analyzes only a few matches for quick testing
3. **`fetch_all_pl_2015_2016_data.py`** - Fetches all raw data (events) from all matches
4. **`quick_fetch_example.py`** - Simple example to test API access

## 🚀 How to Use

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Test that everything works

```bash
python3 test_player_stats.py
```

This analyzes only 5 matches and takes ~2 minutes.

### 3. Generate full player statistics (SMART version)

```bash
python3 generate_player_stats.py
```

🧠 **Smart feature**: The script will first search for existing event data and offer to use it (saves 20-30 minutes!). If none is found, it fetches new data from the API.

### 🚀 Recommended workflow:

```bash
# Step 1: Fetch raw data first (do this once, 20-30 min)
python3 fetch_all_pl_2015_2016_data.py

# Step 2: Generate player statistics (uses existing data, 2-3 min!)
python3 generate_player_stats.py
```

**Result**: Total time reduced from 40-60 minutes to 20-35 minutes! 🎉

## 📊 What do you get?

### Output files:

- `pl_2015_2016_player_stats_full_[timestamp].csv` - Complete statistics with all details
- `pl_2015_2016_player_stats_simple_[timestamp].csv` - Simplified overview with main statistics
- `pl_2015_2016_top_scorers_[timestamp].csv` - Top 20 goal scorers

### Statistics included:

#### ⚽ Attacking Statistics

- Goals scored
- Shots (total, on target, off target, blocked)
- Expected Goals (xG)
- Assists and key passes
- Headers

#### 🎯 Passing Statistics

- Passes attempted/completed
- Pass completion percentage
- Short/medium/long passes
- Forward/backward/sideways passes
- Crosses

#### 🏃‍♂️ Dribbling Statistics

- Dribbles attempted/completed
- Dribbling success percentage

#### 🛡️ Defensive Statistics

- Tackles attempted/won
- Interceptions
- Clearances
- Blocks
- Pressures

#### 🟨 Discipline

- Fouls committed/won
- Yellow cards
- Red cards

#### 📍 Positional Data

- Average position (x,y coordinates)
- Ball touches
- Ball losses

#### 📈 Per-Match Statistics

- Passes per match
- Shots per match
- Goals per match
- Assists per match

## 🎓 Educational Explanation

### The Problem:

Football analysis requires detailed player statistics to understand performance and compare players.

### The Solution:

1. **Data Fetching**: Uses StatsBomb API to retrieve event data
2. **Aggregation**: Converts raw events into meaningful statistics
3. **Categorization**: Organizes statistics into logical groups
4. **Normalization**: Calculates per-match and percentage metrics

### Relevance for CIT4620:

- **Feature Engineering**: Converting raw data into ML features
- **Data Preprocessing**: Cleaning and structuring large datasets
- **Statistical Analysis**: Calculating derived metrics and summaries
- **Big Data**: Handling ~760,000 events from 380 matches

## 🔍 Usage Example

```python
import pandas as pd

# Load player statistics
stats = pd.read_csv('data/pl_2015_2016_player_stats_simple_[timestamp].csv')

# Find top scorers
top_scorers = stats.nlargest(10, 'goals_scored')
print(top_scorers[['player_name', 'team', 'goals_scored', 'assists']])

# Players with best passing percentage (min 1000 passes)
accurate_passers = stats[stats['passes_attempted'] >= 1000]
best_passers = accurate_passers.nlargest(10, 'pass_completion_rate')

# Most creative players
creative = stats.nlargest(10, 'key_passes')
```

## 📈 Example Results

### Top Scorers (expected):

1. **Harry Kane** - Tottenham
2. **Sergio Agüero** - Manchester City
3. **Jamie Vardy** - Leicester City (championship season!)
4. **Romelu Lukaku** - Everton
5. **Olivier Giroud** - Arsenal

### Best Passing Percentage:

- Central defenders and defensive midfielders
- Goalkeepers (short passes)

### Most Creative Players:

- Attacking midfielders
- Wingers with many crosses

## 🚨 Tips and Warnings

### Performance:

- Full analysis takes a long time - be patient!
- Test first with `test_player_stats.py`
- Scripts use API rate limiting to avoid blocking

### Data Quality:

- StatsBomb data is very detailed and accurate
- Some matches may be missing certain event types
- Position data is in StatsBomb's coordinate system (120x80)

### File Sizes:

- Full statistics: ~2-5 MB
- Raw data (if fetched): ~200-500 MB

## 🔧 Troubleshooting

### Common Problems:

1. **Import error**: Install `statsbombpy` with `pip install statsbombpy`
2. **API timeout**: Try again later, or increase the pause time in the script
3. **Missing data**: Some matches may have limited data available

### Debug:

```bash
python3 -c "import statsbombpy; print('StatsBomb OK')"
python3 quick_fetch_example.py  # Test API access
```

## 📚 Further Development

### Possible Extensions:

- Heatmaps based on positional data
- Player comparison and clustering
- Predictive models for player performance
- Integration with other seasons/leagues

### For CIT4620 Projects:

- Use statistics as features for ML models
- Implement similarity search based on player styles
- Create neural networks for player performance prediction

---

**Created by AI Assistant for CIT4620 - Evolutionary AI and Robotics**  
_OsloMet - September 2025_
