from .default import Config
import os

class Config(Config):
    DEBUG = False
    DATABASE = {
        'host': os.getenv('PGHOST', 'monorail.proxy.rlwy.net'),
        'database': os.getenv('PGDATABASE', 'railway'),
        'user': os.getenv('PGUSER', 'postgres'),
        'password': os.getenv('PGPASSWORD', 'uCvSdWUYewpxUAqxuQFocMlYkfQWVzJB'),
        'port': int(os.getenv('PGPORT', 38750)),
    }
