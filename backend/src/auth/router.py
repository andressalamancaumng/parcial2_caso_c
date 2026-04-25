from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
import psycopg2
from src.auth.service import hash_password, verify_password, create_token, DB_CONFIG, JWT_SECRET
from datetime import datetime

router = APIRouter()

class RegisterBody(BaseModel):
    cedula: str
    nombre: str
    email: EmailStr
    telefono: str
    password: str

class LoginBody(BaseModel):
    cedula: str
    password: str

@router.post("/register")
def register(body: RegisterBody):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    pwd = hash_password(body.password)
    # ← VULNERABLE: SQL injection
    cursor.execute(
        f"INSERT INTO ciudadanos (cedula,nombre,email,telefono,password_hash) "
        f"VALUES ('{body.cedula}','{body.nombre}','{body.email}','{body.telefono}','{pwd}')"
    )
    conn.commit(); conn.close()
    return {"cedula": body.cedula, "mensaje": "Registro exitoso"}

@router.post("/login")
def login(body: LoginBody, request: Request):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    pwd = hash_password(body.password)
    # ← VULNERABLE: SQL injection
    cursor.execute(
        f"SELECT id,nombre,role,estado FROM ciudadanos "
        f"WHERE cedula='{body.cedula}' AND password_hash='{pwd}'"
    )
    usuario = cursor.fetchone()

    if not usuario:
        # ← VULNERABLE: mensajes diferentes revelan si la cedula existe
        cursor.execute(f"SELECT id FROM ciudadanos WHERE cedula='{body.cedula}'")
        existe = cursor.fetchone(); conn.close()
        if existe: raise HTTPException(401, "Contrasena incorrecta")
        raise HTTPException(401, "Cedula no registrada")

    conn.close()
    # ← VULNERABLE: cedula completa en el token
    token = create_token({"user_id":usuario[0],"nombre":usuario[1],
                          "cedula":body.cedula,"role":usuario[2]})
    # ← VULNERABLE: log con cedula completa
    print(f"[LOGIN] cedula={body.cedula} ip={request.client.host}")
    return {"token": token}
