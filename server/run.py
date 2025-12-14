from dotenv import load_dotenv # Import this
load_dotenv()                 # Call it at the very top

from app import create_app
from app.config import DevelopmentConfig  # Make sure your config.py exists

app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
