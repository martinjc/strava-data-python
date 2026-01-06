# Strava Data Python

Tools for authenticating with the Strava API, downloading your activity data, and generating beautiful visualizations.

## Features

-   **OAuth2 Authentication**: Securely authenticate with your Strava account.
-   **Incremental Downloading**: Downloads only new activities since the last run to save time and API quota.
-   **Local Caching**: Stores activities in a local JSON file (`data/activities.json`).
-   **Data Visualization**: Generates high-quality PNG images using **D3.js** and **Playwright**.
    -   **Monthly Distance**: Bar charts (All-Time & Yearly).
    -   **Trailing Distance**: Line charts for trailing 365 days (All-Time) and 90 days (Yearly).
    -   **Pace vs Distance**: Scatter plots (All-Time & Yearly).
    -   **Heatmaps**: Weekly distance (All-Time) and Daily Calendar (Yearly).
    -   **Personal Records**: Table of fastest times for standard distances.
    -   **Area Maps**: "Cardiff Runs" map showing run density in a specific area.
    -   **Latest Run**: Map and statistics for your most recent activity.
    -   **Inspirational Quotes**: Generates random motivational images with running quotes.

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
    pip install stravalib python-dotenv pandas playwright
    playwright install
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

### 3. Generate Visualizations

There are two scripts for generating images.

**Generate Data Plots:**
Creates all statistical charts and maps (Monthly, Trailing, Heatmaps, Maps, PRs).
```bash
python plots/generate_plots.py
```
-   Outputs are saved to `plots/output/`.

**Generate Inspirational Quote:**
Creates a single random inspirational quote image.
```bash
python plots/generate_quote.py
```
-   Detailed output found in `plots/output/inspirational_quote.png`.

## Project Structure

-   `strava/`: Scripts for API interaction (`authenticate.py`, `download_activities.py`).
-   `data/`: Stores the downloaded activity data (`activities.json`).
-   `plots/`: Visualization logic.
    -   `generate_plots.py`: Main plot generation script.
    -   `generate_quote.py`: Quote image generation script.
    -   `templates/`: HTML/D3.js templates and CSS.
    -   `output/`: Generated PNG images (excluded from git).
-   `quotes/`: Source file for inspirational quotes.
-   `running-images/`: Background images for quotes.

## License
[MIT](LICENSE)
