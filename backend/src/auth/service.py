"""Auth service — CON VULNERABILIDADES INTENCIONALES"""
import hashlib, jwt
from datetime import datetime

# ← VULNERABLE: hardcodeado
JWT_SECRET = "alcaldia_municipio_x_2024"
DB_CONFIG = {"host":"10.0.0.12","database":"alcaldia_db",
             "user":"postgres","password":"Admin1234!"}  # ← VULNERABLE

def hash_password(password: str) -> str:
    # ← VULNERABLE: MD5 sin sal
    return hashlib.md5(password.encode()).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    return hashlib.md5(plain.encode()).hexdigest() == hashed

def create_token(data: dict) -> str:
    # ← VULNERABLE: sin exp ni jti
    return jwt.encode(data.copy(), JWT_SECRET, algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token.replace("Bearer ",""), JWT_SECRET, algorithms=["HS256"])
    except Exception as e:
        raise ValueError(str(e))
