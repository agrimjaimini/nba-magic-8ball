from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import ast
import os
import re

app = Flask(__name__, static_folder="build", template_folder="build")
CORS(app)


PLAYER_HEADSHOTS = {
    "LeBron James": "https://cdn.nba.com/headshots/nba/latest/260x190/2544.png",
    "Stephen Curry": "https://cdn.nba.com/headshots/nba/latest/260x190/201939.png",
    "Kevin Durant": "https://cdn.nba.com/headshots/nba/latest/260x190/201142.png",
    "Luka Dončić": "https://cdn.nba.com/headshots/nba/latest/260x190/1629029.png",
    "Jayson Tatum": "https://cdn.nba.com/headshots/nba/latest/260x190/1628369.png",
    "Joel Embiid": "https://cdn.nba.com/headshots/nba/latest/260x190/203954.png",
    "Nikola Jokić": "https://cdn.nba.com/headshots/nba/latest/260x190/203999.png",
    "Shai Gilgeous-Alexander": "https://cdn.nba.com/headshots/nba/latest/260x190/1628983.png",
    "Michael Jordan" : "https://cdn.nba.com/headshots/nba/latest/260x190/893.png",
    "Kobe Bryant" : "https://cdn.nba.com/headshots/nba/latest/260x190/977.png",
    "Shaquille O'Neal" : "https://cdn.nba.com/headshots/nba/latest/260x190/406.png",
    "Magic Johnson" : "https://cdn.nba.com/headshots/nba/latest/260x190/77142.png",
    "Larry Bird" : "https://cdn.nba.com/headshots/nba/latest/260x190/1449.png",
    "Wilt Chamberlain" : "https://cdn.nba.com/headshots/nba/latest/260x190/76375.png",
    "Bill Russell" : "https://cdn.nba.com/headshots/nba/latest/260x190/78049.png",
    "Kareem Abdul-Jabbar" : "https://cdn.nba.com/headshots/nba/latest/260x190/76003.png",
    "Tim Duncan" : "https://cdn.nba.com/headshots/nba/latest/260x190/1495.png",
    "Giannis Antetokounmpo": "https://cdn.nba.com/headshots/nba/latest/260x190/203507.png"
}

model = SentenceTransformer("backend/models/nba_fine_tuned_model")

def fix_embedding_str(s):
    s = s.strip()  # Remove leading/trailing whitespace
    # Ensure the string starts with '[' and ends with ']'
    if not s.startswith('['):
        s = '[' + s
    if not s.endswith(']'):
        s = s + ']'
    # Replace one or more whitespace characters between numbers with a comma
    s = re.sub(r'\s+', ',', s)
    return s

# Apply the fix before literal_eval

df = pd.read_csv("backend/data/nba_embeddings.csv")
df["embedding"] = df["embedding"].apply(ast.literal_eval)
embeddings_matrix = np.array(df["embedding"].tolist(), dtype=np.float32)

def predict_player(query, metric="cosine"):
    query_embedding = model.encode(query).reshape(1, -1)
    if metric == "cosine":
        query_norm = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        embeddings_norm = embeddings_matrix / np.linalg.norm(embeddings_matrix, axis=1, keepdims=True)
        scores = np.dot(embeddings_norm, query_norm.T).flatten()
        best_idx = np.argmax(scores)
        result_score = scores[best_idx]
    
    name = df.iloc[best_idx]['player']
    result = {"name": name, "score": f"{result_score:.4f}", "headshot": PLAYER_HEADSHOTS[name]}
    return result


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
    question = data["text"]
    result = predict_player(question)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)