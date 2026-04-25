from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.router import router as auth_router
from src.tramites.router import router as tramite_router
from src.pagos.router import router as pago_router

app = FastAPI(title="Alcaldia Digital API", version="1.0.0")
app.add_middleware(CORSMiddleware,
    allow_origins=["https://alcaldia-grupoN.lab.umng.edu.co"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tramite_router, prefix="/api", tags=["tramites"])
app.include_router(pago_router, prefix="/api", tags=["pagos"])
