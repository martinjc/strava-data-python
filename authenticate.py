import os
import time
import json
from dotenv import load_dotenv
from stravalib.client import Client

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')

if not CLIENT_ID or not CLIENT_SECRET:
    print("Error: STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET must be set in .env file.")
    exit(1)

def authenticate():
    client = Client()
    
    # Create the authorization URL
    # We use localhost as the redirect URI for simplicity in this local script flow
    authorize_url = client.authorization_url(
        client_id=CLIENT_ID,
        redirect_uri='http://localhost:8000/authorized',
        scope=['read_all', 'profile:read_all', 'activity:read_all']
    )
    
    print(f"\nPlease visit this URL to authorize the application:\n\n{authorize_url}\n")
    print("After authorizing, you will be redirected to a URL like 'http://localhost:8000/authorized?state=&code=...'")
    print("Copy the 'code' parameter value from that URL and paste it here.")
    
    code = input("\nEnter the code: ")
    
    # Exchange code for tokens
    try:
        token_response = client.exchange_code_for_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            code=code
        )
        
        # Save tokens to file
        token_data = {
            'access_token': token_response['access_token'],
            'refresh_token': token_response['refresh_token'],
            'expires_at': token_response['expires_at']
        }
        
        with open('strava_tokens.json', 'w') as f:
            json.dump(token_data, f, indent=4)
            
        print("\nAuthentication successful! Tokens saved to 'strava_tokens.json'.")
        
    except Exception as e:
        print(f"\nError during authentication: {e}")

if __name__ == "__main__":
    authenticate()
