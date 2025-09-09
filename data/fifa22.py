import pandas as pd

# Sett riktig filnavn (tilpass hvis det heter noe annet hos deg)
df = pd.read_csv("data/players_22.csv")

# Se på de første radene
print(df.shape)
print(df.columns.tolist())
df.head()