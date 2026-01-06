import os
import time
import threading
import random
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

# Configuration
PORT = 8001 # Use a different port to avoid potential conflicts if both run
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

def generate_quote():
    # Start server in a thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Allow server to start
    time.sleep(1)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": 600, "height": 448})
        
        try:
            # 1. Read Quotes
            quotes_path = os.path.join(ROOT_DIR, "quotes", "quotes.md")
            with open(quotes_path, "r") as f:
                lines = f.readlines()
            
            # Filter valid quotes and parse
            valid_quotes = []
            for line in lines:
                line = line.strip()
                if not line: continue
                # Split by em-dash, en-dash, or hyphen
                parts = []
                if "—" in line: parts = line.split("—")
                elif "–" in line: parts = line.split("–")
                elif "-" in line: parts = line.split("-")
                
                if len(parts) >= 2:
                    q_text = parts[0].strip().strip('"')
                    q_auth = parts[1].strip()
                    valid_quotes.append((q_text, q_auth))
            
            # 2. Read Images
            images_dir = os.path.join(ROOT_DIR, "running-images")
            images = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            # 3. Fonts
            fonts = ['Arial', 'Helvetica', 'Georgia', 'Times New Roman', 'Verdana', 'Courier New', 'Impact']

            if valid_quotes and images:
                sel_quote, sel_author = random.choice(valid_quotes)
                sel_image = random.choice(images)
                sel_font = random.choice(fonts)
                
                # URL Encode params
                params = {
                    "image": sel_image,
                    "quote": sel_quote,
                    "author": sel_author,
                    "font": sel_font
                }
                query_string = urllib.parse.urlencode(params)
                
                url = f"http://localhost:{PORT}/plots/templates/inspirational_quote.html?{query_string}"
                print(f"Generating Inspirational Quote...")
                page.goto(url)
                
                page.wait_for_selector(".quote", timeout=5000)
                time.sleep(0.5)
                page.screenshot(path=os.path.join(OUTPUT_DIR, "inspirational_quote.png"))
                print("Saved inspirational_quote.png")
            else:
                print("Skipping Inspirational Quote: Missing quotes or images.")

        except Exception as e:
            print(f"Error generating inspirational_quote: {e}")
        
        browser.close()

if __name__ == "__main__":
    generate_quote()
