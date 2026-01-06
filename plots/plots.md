# Plots

This directory contains scripts to generate visualizations of the Strava activity data.

## Monthly Distance
-   **Template**: `monthly_distance.html`
-   **Output**: `output/monthly_distance.png`
-   **Description**: A D3.js bar chart showing the total distance run per month.
-   **Dimensions**: 600x448

## Trailing 365 Days Distance
-   **Template**: `trailing_365.html`
-   **Output**: `output/trailing_365.png`
-   **Description**: A D3.js line chart showing the total distance covered in the 365 days prior.
-   **Dimensions**: 600x448

## Pace vs Distance
-   **Template**: `pace_vs_distance.html`
-   **Output**: `output/pace_vs_distance.png`
-   **Description**: A D3.js scatter plot showing average pace vs distance for all runs.
-   **Dimensions**: 600x448

## Weekly Heatmap
-   **Template**: `weekly_heatmap.html`
-   **Output**: `output/weekly_heatmap.png`
-   **Description**: A D3.js heatmap showing total weekly distance (Year vs Week No).
-   **Dimensions**: 600x448

## Latest Run Map
-   **Template**: `latest_run.html`
-   **Output**: `output/latest_run.png`
-   **Description**: A map of the most recent run with statistics (Distance, Pace, Time).
-   **Dimensions**: 600x448

## Personal Records Table
-   **Template**: `personal_records.html`
-   **Output**: `output/personal_records_*.png`
-   **Description**: A table listing fastest run times for standard distances (1mi, 5k, 10k, etc), with count of runs. Generated for all time and per year.
-   **Dimensions**: 600x448

## Area Map
-   **Template**: `area_map.html`
-   **Output**: `output/area_map_*.png`
-   **Description**: A map showing all runs starting within a specific geographic bounding box, overlaid to show density, with summary stats. Generated for all time and per year.
-   **Dimensions**: 600x448

## Inspirational Quote
-   **Template**: `inspirational_quote.html`
-   **Output**: `output/inspirational_quote.png`
-   **Description**: A randomly generated motivational image featuring a background from `running-images/` and a quote from `quotes/quotes.md`.
-   **Dimensions**: 600x448

## Generation
Run `python plots/generate_quote.py` to generate the inspirational quote image.

Run `python plots/generate_plots.py` to generate all other plots.
