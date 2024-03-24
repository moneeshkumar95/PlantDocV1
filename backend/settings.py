import os
from datetime import timedelta


from dotenv import load_dotenv

# Load the .env
load_dotenv()

ENV: str = os.getenv("ENV", "Dev")
APP_NAME: str = "Plant Disease Classification V1"

# For JWT configuration
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM: str = "HS256"
JWT_ACCESS_TOKEN_EXPIRE = timedelta(days=1)

# AWS Configs
AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME: str = os.getenv("AWS_REGION_NAME")
S3_BUCKET: str = os.getenv("S3_BUCKET")
S3_LOCATION: str = os.getenv("S3_LOCATION")

# GOOGLE API
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
GOOGLE_GEOCODE_BASE_URL:str = "https://maps.googleapis.com/maps/api/geocode/json"

AWS_KWARGS = dict(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)
