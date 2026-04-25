"""Tests de auth Caso C"""
import pytest

def test_login_mensajes_diferentes():
    """
    DOCUMENTA LA VULNERABILIDAD: mensajes de error diferentes revelan si la cedula existe.
    Despues de corregir, ambos deben retornar el mismo mensaje.
    TODO: implementar con httpx.AsyncClient
    """
    pass

def test_cedula_en_token():
    """TODO: verificar que el token no contiene la cedula completa"""
    pass

def test_pago_no_almacena_tarjeta():
    """TODO: verificar que el endpoint de pago no persiste datos de tarjeta"""
    pass
