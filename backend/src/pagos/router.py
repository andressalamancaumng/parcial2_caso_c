from fastapi import APIRouter, Header, HTTPException
import psycopg2
from src.auth.service import decode_token, DB_CONFIG

router = APIRouter()

@router.post("/pago/impuesto")
def procesar_pago(data: dict, authorization: str = Header(None)):
    if not authorization: raise HTTPException(401, "No autorizado")
    payload = decode_token(authorization)
    monto          = data.get("monto")
    matricula      = data.get("matricula_inmobiliaria")
    numero_tarjeta = data.get("numero_tarjeta")
    cvv            = data.get("cvv")

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    # ← VULNERABLE: almacena numero de tarjeta y CVV en la BD
    cursor.execute(
        "INSERT INTO transacciones (ciudadano_id,monto,matricula,tarjeta,cvv,estado) "
        "VALUES (%s,%s,%s,%s,%s,'aprobado')",
        (payload["user_id"], monto, matricula, numero_tarjeta, cvv)
    )
    conn.commit(); conn.close()
    # ← VULNERABLE: retorna CVV en la respuesta
    return {"mensaje":"Pago procesado","tarjeta_usada":numero_tarjeta,"cvv_confirmado":cvv}
