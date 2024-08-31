import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'root'
    DB_NAME = os.environ.get('DB_NAME') or 'backend'
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}