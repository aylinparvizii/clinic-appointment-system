from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


# JWT settings
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30