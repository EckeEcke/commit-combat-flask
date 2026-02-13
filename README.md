# Commit Combat Flask

## Project Description
Commit Combat Flask is a backend application for Commit Combat web game, that gamifies the experience of managing Git commits. It allows users to engage in friendly competition using their own github accounts.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/EckeEcke/commit-combat-flask.git
   cd commit-combat-flask
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Guide
1. Start the application:
   ```bash
   flask run
   ```
2. Open your web browser and navigate to `http://127.0.0.1:5000`.

## API Endpoints

### 1. Get User Avatar

**GET** `/image-proxy/<username>`

- **Description**: Proxies and returns a GitHub user's avatar image. This endpoint acts as a CORS-compatible proxy to GitHub's avatar service.
- **Parameters**:
  - `username` (string, required): GitHub username whose avatar is to be retrieved
- **Responses**:
  - `200`: Avatar image in PNG format
  - `404`: Image not found or user does not exist

**Example:**
```bash
GET /image-proxy/octocat
```

---

### 2. Get Battle Data

**GET** `/get-battle/<p1>`  
**GET** `/get-battle/<p1>/<p2>`

- **Description**: Fetches GitHub contribution data for the last 14 days for one or two players. Returns contribution grids ("shield grids") for use in the Commit Combat game.
- **Parameters**:
  - `p1` (string, required): GitHub username of the first player
  - `p2` (string, optional): GitHub username of the second player (opponent)
- **Responses**:
  - `200`: JSON object with player and enemy shield grids
  - `404`: One or both users not found
  - `400`: GitHub API error

**Example response:**
```json
{
  "player": {
    "name": "octocat",
    "shield_grid": [
      [2, 1, 4, 2, 2, 0, 2],
      [1, 3, 0, 2, 1, 4, 2]
    ]
  },
  "enemy": {
    "name": "other-user",
    "shield_grid": [
      [3, 0, 0, 1, 0, 1, 4],
      [2, 1, 2, 3, 0, 2, 1]
    ]
  }
}
```

**Error response example:**
```json
{
  "error": "User not found",
  "message": "Following GitHub-Users do not exist: invalid-user",
  "missing_users": ["invalid-user"]
}
```

---

## Configuration

### Required Environment Variables

- `GITHUB_TOKEN`: GitHub Personal Access Token for API authentication