import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from app import create_app, db

env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
    
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)