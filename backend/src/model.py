from sentence_transformers import SentenceTransformer, losses, InputExample
from torch.utils.data import DataLoader
import pandas as pd

# Load your training data (which now only contains positive pairs)
df = pd.read_csv("backend/data/training_pairs.csv")

# Filter out pairs with empty or null strings
df = df.dropna(subset=["text1", "text2"])
df = df[(df["text1"].str.strip() != "") & (df["text2"].str.strip() != "")]

# Create InputExamples without labels (they are implicitly positive pairs)
train_examples = [
    InputExample(texts=[row["text1"], row["text2"]])
    for _, row in df.iterrows()
]

# Create a DataLoader for batching
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=32)

# Initialize the model (you can experiment with stronger models such as "all-mpnet-base-v2")
model = SentenceTransformer("all-MiniLM-L12-v2")

# Use MultipleNegativesRankingLoss which automatically uses other batch samples as negatives.
train_loss = losses.MultipleNegativesRankingLoss(model)

# Train the model
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=4,
    warmup_steps=100,
    show_progress_bar=True,
    output_path="backend/models/nba_fine_tuned_model_build2"
)
