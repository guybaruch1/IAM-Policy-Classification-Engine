import os
import sys
from dotenv import load_dotenv

# Get the API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    print("Please create a .env file based on .env.example and add your API key.")
    sys.exit(1)
