import json
import os

SCORES_FILE = "Jour 1/highscores.json"

def load_scores():
    """Load high scores from file"""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
            raise
    return []

def save_score(name, exp, battles_won):
    """Save a new score to the file"""
    scores = load_scores()
    scores.append({
        "name": name,
        "exp": exp,
        "battles_won": battles_won
    })
    # Sort by EXP descending
    scores.sort(key=lambda x: x["exp"], reverse=True)
    # Keep only top 10
    scores = scores[:10]
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def display_top_scores():
    """Display the top 3 high scores"""
    scores = load_scores()
    if scores:
        print(f"\n{'='*50}")
        print("🏆 TOP 3 HIGH SCORES 🏆")
        print(f"{'='*50}")
        for i, score in enumerate(scores[:3], 1):
            if i == 1:
                medal = "🥇"
            elif i == 2:
                medal = "🥈"
            else:
                medal = "🥉"
            print(f"{medal} {i}. {score['name']}: {score['exp']} EXP ({score['battles_won']} battles won)")
        print(f"{'='*50}\n")
    else:
        print("\n🏆 No high scores yet! Be the first!\n")