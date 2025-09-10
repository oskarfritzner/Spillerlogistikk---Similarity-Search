# ⚽ Advanced Player Style Similarity Search

## 🎯 Project Overview

An advanced similarity search system for football players based on **actual match performance data** rather than theoretical ratings. This project analyzes playing styles, movement patterns, and ball usage to find similar players and budget-friendly alternatives.

Built with **StatsBomb Premier League 2015/2016** data for the **ACIT4610 - Evolutionary AI and Robotics** course.

---

## 🚀 Project Goals

### Primary Objectives:
1. **Playing Style Similarity** - Find players with similar on-field behavior
2. **Budget Optimization** - Identify cheaper alternatives with similar playing styles  
3. **Multi-Objective Optimization** - Pareto front analysis balancing price vs similarity/quality
4. **Educational Implementation** - Build everything step-by-step to understand core concepts

### Key Innovations:
- **Real Match Data** instead of FIFA ratings
- **Movement Pattern Analysis** using position and distance data
- **Ball Usage Profiling** through passing, dribbling, and possession statistics
- **Evolutionary Algorithms** for feature weight optimization

---

## 📊 Data Features

Our StatsBomb dataset includes **50+ detailed features** per player:

### 🏃‍♂️ Movement & Positioning
- `avg_position_x`, `avg_position_y` - Average field position
- `distance_covered` - Total distance per game
- `pressure_events` - Defensive pressure applied

### ⚽ Ball Usage & Passing Style  
- `short_passes`, `medium_passes`, `long_passes` - Pass type distribution
- `forward_passes`, `backward_passes`, `sideways_passes` - Pass direction
- `pass_completion_rate` - Passing accuracy
- `key_passes`, `assists` - Creative contribution

### 🎯 Playing Intensity
- `dribbles_attempted`, `dribbles_completed` - Ball-carrying ability
- `ball_receipts`, `ball_recoveries` - Ball involvement
- `dispossessed`, `miscontrols` - Ball security
- `tackles_won`, `interceptions`, `clearances` - Defensive actions

### 📈 Performance Metrics
- `goals_per_game`, `assists_per_game` - Offensive output
- `shots_total`, `shot_accuracy` - Shooting profile
- `total_xg` - Expected goals (quality of chances)

---

## 🛠️ Technology Stack

### Core ML & Similarity
```python
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
```

### Multi-Objective Optimization
```python
from pymoo.algorithms.moo.nsga2 import NSGA2  # Pareto front optimization
from scipy.optimize import differential_evolution
```

### Evolutionary Algorithms
```python
from deap import base, creator, tools, algorithms  # Feature weight optimization
```

### Data & Visualization
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  # Interactive visualizations
```

---

## 🏗️ Implementation Plan

### Phase 1: Foundation (Current)
- [x] **Project Setup** - Basic structure and data loading
- [ ] **Data Loading** - Import and clean StatsBomb data
- [ ] **Feature Analysis** - Understand playing style dimensions
- [ ] **Basic Similarity** - Simple cosine similarity implementation

### Phase 2: Playing Style Profiling
- [ ] **Style Feature Selection** - Identify key behavioral indicators
- [ ] **Player Clustering** - Group players by playing style
- [ ] **Style Visualization** - Radar charts and position heatmaps
- [ ] **Similarity Testing** - Test with known players (Kane, Özil, Kanté)

### Phase 3: Advanced Similarity Search
- [ ] **Weighted Similarity** - Different importance for different features
- [ ] **Multi-Metric Comparison** - Cosine vs Euclidean vs Custom metrics
- [ ] **Position-Aware Search** - Consider field position in similarity
- [ ] **Performance Validation** - Test accuracy with expert knowledge

### Phase 4: Budget Optimization
- [ ] **Value Estimation Model** - Predict player market value
- [ ] **Budget-Constrained Search** - Find alternatives within price range
- [ ] **Value-for-Money Scoring** - Performance per unit cost
- [ ] **Risk Assessment** - Age, injury, form factors

### Phase 5: Multi-Objective Optimization
- [ ] **Pareto Front Analysis** - Price vs Quality vs Similarity
- [ ] **NSGA-II Implementation** - Multi-objective genetic algorithm
- [ ] **Interactive Selection** - Let users choose from Pareto optimal solutions
- [ ] **Sensitivity Analysis** - How robust are recommendations?

### Phase 6: Evolutionary Feature Learning
- [ ] **Genetic Algorithm** - Evolve optimal feature weights
- [ ] **Fitness Functions** - Define what makes a good similarity match
- [ ] **Population Diversity** - Maintain varied solution approaches
- [ ] **Convergence Analysis** - Track algorithm performance

---

## 📁 Project Structure


advanced_similarity/
├── README.md # This file
├── player_style_similarity.py # Main similarity engine
├── data_loader.py # Data import and preprocessing
├── style_profiler.py # Playing style analysis
├── budget_optimizer.py # Budget-aware recommendations
├── pareto_optimizer.py # Multi-objective optimization
├── evolutionary_features.py # GA for feature weights
├── visualizations.py # Plotting and charts
├── tests/ # Unit tests
│ ├── test_similarity.py
│ ├── test_budget.py
│ └── test_optimization.py
└── examples/ # Usage examples
├── basic_similarity_demo.py
├── budget_search_demo.py
└── pareto_analysis_demo.py

---

## 🎯 Key Learning Objectives

### Computational Intelligence Concepts:
1. **Similarity Metrics** - Understanding distance measures in high-dimensional spaces
2. **Feature Engineering** - Selecting and weighting relevant attributes
3. **Unsupervised Learning** - Clustering players by behavior patterns
4. **Multi-Objective Optimization** - Balancing competing objectives
5. **Evolutionary Algorithms** - Using GA for parameter optimization

### Practical Skills:
1. **Real Data Handling** - Working with messy, real-world sports data
2. **Performance Evaluation** - Validating ML models against domain expertise
3. **Interactive Systems** - Building user-friendly recommendation tools
4. **Visualization** - Communicating complex results clearly

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy scikit-learn matplotlib seaborn plotly pymoo deap
```

### Quick Start
```bash
cd advanced_similarity
python3 player_style_similarity.py
```

### Testing Similarity Search
```python
from player_style_similarity import find_similar_players

# Find players similar to Harry Kane
similar_players = find_similar_players("Harry Kane", method='cosine', n_results=5)
print(similar_players)
```

---

## 📈 Success Metrics

### Technical Validation:
- **Similarity Accuracy** - Do similar players make football sense?
- **Budget Optimization** - Can we find 80% similarity at 50% cost?
- **Pareto Efficiency** - Are our trade-offs mathematically optimal?
- **Algorithm Performance** - Convergence speed and stability

### Football Domain Validation:
- **Expert Agreement** - Do scouts agree with our recommendations?
- **Position Consistency** - Do we find players in sensible positions?
- **Style Coherence** - Are playing styles logically grouped?
- **Transfer Success** - Would these recommendations work in practice?

---

## 🔮 Future Extensions

### Advanced Analytics:
- **Temporal Analysis** - How do playing styles evolve over time?
- **Team Chemistry** - How do player combinations work together?
- **Injury Risk** - Predict injury likelihood from playing style
- **Performance Prediction** - Forecast future player development

### Technical Enhancements:
- **Deep Learning** - Neural networks for pattern recognition
- **Real-time Analysis** - Live match similarity tracking
- **Cross-League Comparison** - Compare players across different leagues
- **Mobile App** - User-friendly interface for scouts

---

## 👥 Contributors

- **Student**: [Your Name] - Implementation and analysis
- **AI Assistant**: Technical guidance and methodology
- **Course**: ACIT4610 - Evolutionary AI and Robotics, OsloMet

---

## 📝 License

Educational project for ACIT4610. StatsBomb data used under their open data license.

---

*"Finding the next hidden gem through the power of data science and evolutionary algorithms"* ⚽🤖