from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env") 
apiToken = os.getenv('API_SECRET')

print(apiToken)