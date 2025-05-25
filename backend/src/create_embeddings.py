import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load fine-tuned model
model = SentenceTransformer("backend/models/nba_fine_tuned_model_build2")

# List of players to encode
df = pd.read_csv("backend/data/nba_clean_data.csv")


# Generate embeddings for each player
text_embeddings = [model.encode(text).tolist() for text in df.text]

# Save as a DataFrame
df = pd.DataFrame({"text": df.text, "embedding": text_embeddings, "player": df.player})
df.to_csv("backend/data/nba_embeddings.csv", index=False)

print(f" Successfully updated nba_embeddings.csv with player embeddings!")
