from search_functions.unified_search import search_players

# Test outfield player
print("Similar to K. De Bruyne (CAM):")
print(search_players("K. De Bruyne", "cam", top_n=5))

# Test goalkeeper
print("\nSimilar to M. Neuer (GK):")
print(search_players("M. Neuer", "gk", top_n=5))