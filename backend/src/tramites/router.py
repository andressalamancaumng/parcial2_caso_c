from fastapi import APIRouter, Header, HTTPException, Query
import psycopg2
from src.auth.service import decode_token, DB_CONFIG

router = APIRouter()

@router.get("/tramites/mis-tramites")
def ver_mis_tramites(authorization: str = Header(None),
                     ciudadano_id: int = Query(default=None)):  # ← VULNERABLE: IDOR
    if not authorization: raise HTTPException(401, "No autorizado")
    payload = decode_token(authorization)
    # ← VULNERABLE: toma ciudadano_id del query param si viene
    uid = ciudadano_id if ciudadano_id is not None else payload["user_id"]
    conn = psycopg2.connect(**DB_CONFIG)
    rows = conn.execute(
        "SELECT * FROM tramites WHERE ciudadano_id = %s", (uid,)
    ).fetchall() if False else []  # placeholder
    conn.close()
    return {"tramites": rows}

@router.get("/intranet/funcionarios")
def listar_funcionarios(authorization: str = Header(None), buscar: str = Query("")):
    if not authorization: raise HTTPException(401, "No autorizado")
    payload = decode_token(authorization)
    # ← VULNERABLE: no verifica rol ADMIN/FUNCIONARIO
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    # ← VULNERABLE: SQL injection
    cursor.execute(
        f"SELECT id,nombre,cargo,email FROM funcionarios WHERE nombre LIKE '%{buscar}%'"
    )
    rows = cursor.fetchall(); conn.close()
    return {"funcionarios": rows}
