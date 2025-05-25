import praw
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into os.environ

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# --- Player Aliases for Nickname/Name Matching ---
def build_player_aliases(players):
    return {
        "Stephen Curry": ["steph", "stephen curry", "curry"],
        "LeBron James": ["lebron", "lebron james", "king james"],
        "Kevin Durant": ["kd", "durant", "kevin durant"],
        "Luka Dončić": ["luka", "doncic", "luka doncic"],
        "Jayson Tatum": ["tatum", "jayson tatum"],
        "Shai Gilgeous-Alexander": ["shai", "gilgeous", "sga", "shai gilgeous", "gilgeous-alexander"],
        "Joel Embiid": ["embiid", "joel embiid"],
        "Nikola Jokić": ["joker", "nikola jokic", "jokic"],
        "Michael Jordan": ["mj", "jordan", "micheal jordan", "air jordan"],
        "Kobe Bryant": ["kobe", "bryant", "black mamba"],
        "Shaquille O'Neal": ["shaq", "diesel", "shaquille o'neal", "shaquille oneal"],
        "Magic Johnson": ["magic", "magic johnson"],
        "Larry Bird": ["larry bird", "larry legend"],
        "Wilt Chamberlain": ["wilt chamberlain", "wilt"],
        "Bill Russell": ["bill russell"],
        "Kareem Abdul-Jabbar": ["kareem", "kareem abdul jabbar"],
        "Tim Duncan": ["tim duncan", "big fundamental"],
        "Giannis Antetokounmpo": ["giannis", "greek freek"]
    }

# --- Detect Players in Comment Text Using Aliases ---
def detect_players_in_comment(comment, player_aliases):
    mentioned_players = set()
    comment_lower = comment.lower()
    for player, aliases in player_aliases.items():
        if any(alias in comment_lower for alias in aliases):
            mentioned_players.add(player)
    return list(mentioned_players)

# --- Scraper Function with Alias Detection ---
def scrape_reddit_comments(player_list, subreddit="nba", num_posts=100, num_comments=10):
    all_comments = []
    # Build the alias dictionary from the player list.
    player_aliases = build_player_aliases(player_list)

    for player in player_list:
        print(f"🔍 Searching for posts about: {player}")
        try:
            posts = reddit.subreddit(subreddit).search(player, sort="top", limit=num_posts)
        except Exception as e:
            print(f" Error searching posts for {player}: {e}")
            continue

        for submission in posts:
            try:
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list()[:num_comments]:
                    text = comment.body
                    # Use the detect function to find which player(s) are mentioned in the comment.
                    detected_players = detect_players_in_comment(text, player_aliases)
                    if detected_players:
                        for detected_player in detected_players:
                            all_comments.append([text, detected_player])
                    else:
                        # Optionally, you can default to the searched player if no alias is detected.
                        # Uncomment the following line if you'd like that behavior.
                        # all_comments.append([text, player])
                        continue
            except Exception as e:
                print(f" Error processing submission/comments: {e}")
                continue

    return pd.DataFrame(all_comments, columns=["text", "player"])

# --- Run as script ---
if __name__ == "__main__":
    players = [
        "Michael Jordan",
        "LeBron James",
        "Kobe Bryant",
        "Shaquille O’Neal",  # Note: Ensure consistent apostrophe style; you may want to use the straight apostrophe (')
        "Magic Johnson",
        "Larry Bird",
        "Wilt Chamberlain",
        "Bill Russell",
        "Kareem Abdul-Jabbar",
        "Tim Duncan",
        "Stephen Curry",
        "Kevin Durant",
        "Giannis Antetokounmpo",
        "Luka Dončić",
        "Nikola Jokić",
        "Shai Gilgeous-Alexander",
        "Jayson Tatum",
        "Joel Embiid"
    ]

    df = scrape_reddit_comments(players, num_posts=100, num_comments=10)
    df.to_csv("backend/data/nba_reddit_comments.csv", index=False)
    print(f" Scraped and saved {len(df)} player-tagged Reddit comments!")
