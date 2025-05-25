import re
import pandas as pd
import nltk
import itertools
import random
from nltk.tokenize import word_tokenize
from sentence_transformers import InputExample

# Download necessary NLTK data
nltk.download('punkt')

# Preprocessing function: cleans and tokenizes the text.
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+|#\w+", "", text)                # Remove mentions/hashtags
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)            # Remove special characters
    tokens = word_tokenize(text)
    return " ".join(tokens)

# Create training pairs using only positive pairs.
# For each player, we pair different comments about the same player.
def create_training_pairs(df, max_pairs_per_player=50):
    train_examples = []
    grouped = df.groupby("player")
    
    for player, group in grouped:
        texts = group["clean_text"].tolist()
        # Only create pairs if there are at least 2 comments
        if len(texts) > 1:
            # Generate all possible positive pairs for this player
            positive_pairs = list(itertools.combinations(texts, 2))
            # Shuffle and limit to a maximum number of pairs per player
            random.shuffle(positive_pairs)
            positive_pairs = positive_pairs[:max_pairs_per_player]
            
            for text1, text2 in positive_pairs:
                # For positive pairs, assign a label of 1.0.
                train_examples.append(InputExample(texts=[text1, text2], label=1.0))
    
    return train_examples

if __name__ == "__main__":
    # Load the scraped Reddit comments.
    df = pd.read_csv("backend/data/nba_reddit_comments.csv")
    
    # Preprocess the text and save the cleaned data.
    df["clean_text"] = df["text"].apply(preprocess_text)
    df.to_csv("backend/data/nba_clean_data.csv", index=False)
    
    # Create positive training pairs
    train_examples = create_training_pairs(df, max_pairs_per_player=50)
    print("Number of training pairs:", len(train_examples))
    
    # Save the training pairs as a CSV file.
    pairs_list = [
        {"text1": ex.texts[0], "text2": ex.texts[1], "label": ex.label}
        for ex in train_examples
    ]
    pairs_df = pd.DataFrame(pairs_list)
    pairs_df.to_csv("backend/data/training_pairs.csv", index=False)
    print("✅ Training pairs saved to training_pairs.csv")
