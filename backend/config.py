import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'cos_study.db')
    GCP_PROJECT = os.environ.get('GCP_PROJECT', 'cos-cloud')
    GCP_ZONE = os.environ.get('GCP_ZONE', 'us-central1-a')
    GCP_INSTANCE = os.environ.get('GCP_INSTANCE', 'demo-cos-instance')
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5001))
    DEMO_MODE = os.environ.get('DEMO_MODE', 'True').lower() in ('true', '1', 't')
