import os
import time
import threading
import subprocess
import sys
import random
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

# Configuration
PORT = 8000
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Project root
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def run_server():
    os.chdir(ROOT_DIR)
    server = HTTPServer(('localhost', PORT), QuietHandler)
    server.serve_forever()

def generate_plots():
    # Start server in a thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Allow server to start
    time.sleep(1)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": 600, "height": 448})
        
        # Dynamic Color Selection
        COLORS = [
            "#4c78a8", # Ocean Blue (Original)
            "#fc4c02", # Strava Orange
            "#59a14f", # Forest Green
            "#e15759", # Berry Red
            "#9c755f", # Brown
            "#b07aa1", # Purple
            "#76b7b2", # Teal
            "#f28e2b", # Orange
        ]
        selected_color = random.choice(COLORS)
        encoded_color = urllib.parse.quote(selected_color)
        print(f"Selected Theme Color: {selected_color}")

        # Plot 1: Monthly Distance
        url = f"http://localhost:{PORT}/plots/templates/monthly_distance.html?color={encoded_color}"
        print(f"Generating {url}...")
        page.goto(url)
        # Wait for chart content (assuming D3 renders inside #chart SVG)
        try:
            page.wait_for_selector("#chart svg g rect", timeout=5000) # Wait for at least one bar
            # Wait a bit more for layout/fonts
            time.sleep(0.5) 
            page.screenshot(path=os.path.join(OUTPUT_DIR, "monthly_distance.png"))
            print("Saved monthly_distance.png")
        except Exception as e:
            print(f"Error generating monthly_distance: {e}")

        # Plot 2: Trailing 365
        url = f"http://localhost:{PORT}/plots/templates/trailing_365.html?color={encoded_color}"
        print(f"Generating {url}...")
        page.goto(url)
        try:
            page.wait_for_selector("#chart svg path.line", timeout=5000)
            time.sleep(0.5)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "trailing_365.png"))
            print("Saved trailing_365.png")
        except Exception as e:
            print(f"Error generating trailing_365: {e}")

        # Plot 3: Pace vs Distance
        url = f"http://localhost:{PORT}/plots/templates/pace_vs_distance.html?color={encoded_color}"
        print(f"Generating {url}...")
        page.goto(url)
        try:
            page.wait_for_selector("#chart svg circle", timeout=5000)
            time.sleep(0.5)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "pace_vs_distance.png"))
            print("Saved pace_vs_distance.png")
        except Exception as e:
            print(f"Error generating pace_vs_distance: {e}")

        # Plot 4: Weekly Heatmap
        url = f"http://localhost:{PORT}/plots/templates/weekly_heatmap.html?color={encoded_color}"
        print(f"Generating {url}...")
        page.goto(url)
        try:
            page.wait_for_selector("#chart svg rect", timeout=5000)
            time.sleep(0.5)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "weekly_heatmap.png"))
            print("Saved weekly_heatmap.png")
        except Exception as e:
            print(f"Error generating weekly_heatmap: {e}")

        # Plot 5: Latest Run Map
        url = f"http://localhost:{PORT}/plots/templates/latest_run.html?color={encoded_color}"
        print(f"Generating {url}...")
        page.goto(url)
        try:
            page.wait_for_selector("#chart svg path.route-path", timeout=5000)
            time.sleep(0.5)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "latest_run.png"))
            print("Saved latest_run.png")
        except Exception as e:
            print(f"Error generating latest_run: {e}")

        # Plot 6: Personal Records (All Time)
        url = f"http://localhost:{PORT}/plots/templates/personal_records.html?color={encoded_color}"
        print(f"Generating {url}...")
        page.goto(url)
        try:
            page.wait_for_selector("#pr-table", timeout=5000)
            time.sleep(0.5)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "personal_records.png"))
            print("Saved personal_records.png")
        except Exception as e:
            print(f"Error generating personal_records: {e}")

        # Plot 7: Area Map (All Time)
        url = f"http://localhost:{PORT}/plots/templates/area_map.html?color={encoded_color}"
        print(f"Generating {url}...")
        page.goto(url)
        try:
            page.wait_for_selector("#chart svg path.route-path", timeout=5000)
            time.sleep(0.5)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "area_map.png"))
            print("Saved area_map.png")
        except Exception as e:
            print(f"Error generating area_map: {e}")

        # Yearly Plots
        import datetime
        current_year = datetime.datetime.now().year
        prev_year = current_year - 1
        
        years = [current_year, prev_year]
        
        # New Templates to generate
        yearly_templates = [
            ("monthly_distance_year.html", "monthly_distance_{year}.png"),
            ("trailing_90_year.html", "trailing_90_{year}.png"),
            ("pace_vs_distance_year.html", "pace_vs_distance_{year}.png"),
            ("daily_heatmap_year.html", "daily_heatmap_{year}.png"),
            ("personal_records.html", "personal_records_{year}.png"),
            ("area_map.html", "area_map_{year}.png")
        ]
        
        for year in years:
            print(f"Generating plots for {year}...")
            for template, output_fmt in yearly_templates:
                url = f"http://localhost:{PORT}/plots/templates/{template}?year={year}&color={encoded_color}"
                output_name = output_fmt.format(year=year)
                print(f"Generating {url} -> {output_name}...")
                
                try:
                    page.goto(url)
                    # Generic wait (using table for PRs, svg for others)
                    page.wait_for_selector("#chart", timeout=5000) 
                    time.sleep(0.5)
                    page.screenshot(path=os.path.join(OUTPUT_DIR, output_name))
                    print(f"Saved {output_name}")
                except Exception as e:
                    print(f"Error generating {output_name}: {e}")

        browser.close()

if __name__ == "__main__":
    generate_plots()
