import requests
from flask import Flask, jsonify
from flask import Flask

app = Flask(__name__)

def get_github_user_info(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route("/")
def home():
    return "Backend running ✅"

@app.route("/get-stats/<username>")
def stats(username):
    data = get_github_user_info(username)
    
    if data:
        game_data = {
            "name": data.get("name"),
            "public_repos": data.get("public_repos"),
            "followers": data.get("followers")
        }
        print(game_data)
        return jsonify(game_data)
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run()