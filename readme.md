# Strava Data Python

Tools for authenticating with the Strava API and downloading your activity data.

## Features

-   **OAuth2 Authentication**: Securely authenticate with your Strava account.
-   **Incremental Downloading**: Downloads only new activities since the last run to save time and API quota.
-   **Local Caching**: Stores activities in a local JSON file (`data/activities.json`).

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd strava-data-python
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install stravalib python-dotenv
    ```

4.  **Configure Credentials**:
    -   Create a `.env` file in the root directory.
    -   Add your Strava API credentials (get them from [Strava Settings](https://www.strava.com/settings/api)):
        ```env
        STRAVA_CLIENT_ID=your_client_id
        STRAVA_CLIENT_SECRET=your_client_secret
        ```

## Usage

### 1. Authenticate

Run the authentication script to generate your tokens. This only needs to be redone if your refresh token expires or is revoked.

```bash
python strava/authenticate.py
```
Follow the instructions to visit the authorization URL and paste the code back into the terminal.

### 2. Download Activities

Run the download script to fetch your latest activities.

```bash
python strava/download_activities.py
```
This will:
-   Refresh your access token automatically if needed.
-   Check `data/activities.json` for the last activity date.
-   Download only new activities from Strava.
-   Update `data/activities.json` with the new data.

## Project Structure

-   `strava/`: Python scripts for authentication and downloading.
-   `data/`: Stores the downloaded activity data.
