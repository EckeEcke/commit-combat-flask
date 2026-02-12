import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

def get_github_contributions(username):
    url = "https://api.github.com/graphql"
    token = os.environ.get('GITHUB_TOKEN')
    
    now = datetime.now()
    start_date = (now - timedelta(days=34)).strftime('%Y-%m-%dT00:00:00Z')
    end_date = now.strftime('%Y-%m-%dT23:59:59Z')

    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "login": username, 
        "from": start_date, 
        "to": end_date
    }
    
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"GitHub API returned status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return "Backend is running! 🛡️"

@app.route("/get-shields/<username>")
def shields(username):
    result = get_github_contributions(username)
    
    if not result or "data" not in result or result["data"]["user"] is None:
        return jsonify({"error": "User nicht gefunden"}), 404
    
    weeks = result['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    
    all_days = []
    for week in weeks:
        for day in week['contributionDays']:
            all_days.append(day['contributionCount'])
    
    last_35_days = all_days[-35:]
    
    shield_grid = []
    for i in range(0, 35, 7):
        shield_grid.append(last_35_days[i:i+7])
        
    return jsonify({
        "username": username,
        "shield_grid": shield_grid
    })

if __name__ == "__main__":
    app.run()