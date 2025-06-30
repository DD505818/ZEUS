import os

API_PORT = int(os.getenv('API_PORT', '8000'))
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
