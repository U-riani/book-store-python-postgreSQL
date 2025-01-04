from .default import Config

class Config(Config):
    DEBUG = True
    DATABASE = {
        'host': 'monorail.proxy.rlwy.net',
        'database': 'railway',
        'user': 'postgres',
        'password': 'uCvSdWUYewpxUAqxuQFocMlYkfQWVzJB',
        'port': 38750
    }
