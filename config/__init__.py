import os

# Determine the environment (development or production)
env = os.getenv('FLASK_ENV', 'development')

if env == 'production':
    from .production import Config
else:
    from .development import Config
