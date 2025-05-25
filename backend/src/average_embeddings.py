import numpy as np
import pandas as pd
import ast

df = pd.read_csv("backend/data/nba_embeddings.csv")
df["embedding"] = df["embedding"].apply(ast.literal_eval)
# Group by player and average embeddings
player_embeddings = (
    df.groupby("player")["embedding"]
      .apply(lambda emb: np.mean(np.vstack(emb), axis=0))
      .reset_index()
)
player_embeddings.to_csv("backend/data/nba_player_embeddings.csv", index=False)
