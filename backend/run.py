import os

from dotenv import load_dotenv

# Load secret .env file
load_dotenv()
# Store credentials
key = os.getenv('user_token')
# Verify it worked
print(key)