import os
import requests
from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

def get_combined_github_data(u1, u2, days_to_fetch):
    url = "https://api.github.com/graphql"
    token = os.environ.get('GITHUB_TOKEN')
    
    now = datetime.now()
    start_date = (now - timedelta(days=days_to_fetch - 1)).strftime('%Y-%m-%dT00:00:00Z')
    end_date = now.strftime('%Y-%m-%dT23:59:59Z')

    query = """
    query($u1: String!, $u2: String!, $from: DateTime!, $to: DateTime!) {
      player: user(login: $u1) { ...Fields }
      enemy: user(login: $u2) { ...Fields }
    }
    fragment Fields on User {
      contributionsCollection(from: $from, to: $to) {
        contributionCalendar {
          weeks {
            contributionDays {
              contributionCount
            }
          }
        }
      }
    }
    """
    
    variables = {
        "u1": u1,
        "u2": u2 if u2 else "",
        "from": start_date,
        "to": end_date
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def process_calendar(user_node, days_to_fetch):
    if not user_node:
        return None
        
    weeks = user_node['contributionsCollection']['contributionCalendar']['weeks']
    all_days = [day['contributionCount'] for week in weeks for day in week['contributionDays']]
    
    relevant_days = all_days[-days_to_fetch:]
    return [relevant_days[i:i+7] for i in range(0, len(relevant_days), 7)]

@app.route('/image-proxy/<username>')
def proxy_avatar(username):
    github_url = f"https://github.com/{username}.png?size=120"
    try:
        res = requests.get(github_url, timeout=5)

        return Response(
            res.content, 
            status=res.status_code, 
            mimetype=res.headers.get('Content-Type', 'image/png')
        )
    except Exception:
        return Response("Image not found", status=404)

@app.route("/get-battle/<p1>")
@app.route("/get-battle/<p1>/<p2>")
def battle(p1, p2=None):
    days = 14
    result = get_combined_github_data(p1, p2, days)
    
    if "errors" in result and not result.get("data"):
        return jsonify({"error": "GitHub API Fehler", "details": result["errors"]}), 400

    data = result.get("data", {})

    missing = []
    if not data or data.get("player") is None: missing.append(p1)
    if p2 and (not data or data.get("enemy") is None): missing.append(p2)
    
    if missing:
        return jsonify({
            "error": "User not found",
            "message": f"Following GitHub-Users do not exist: {', '.join(missing)}",
            "missing_users": missing
        }), 404
    
    return jsonify({
        "player": {
            "name": p1,
            "shield_grid": process_calendar(data.get("player"), days)
        },
        "enemy": {
            "name": p2 if p2 else "No opponent",
            "shield_grid": process_calendar(data.get("enemy"), days)
        }
    })

if __name__ == "__main__":
    app.run()