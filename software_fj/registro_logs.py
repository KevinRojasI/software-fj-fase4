"""Configuración del archivo de logs (única persistencia permitida)."""

import logging
from pathlib import Path

# Carpeta logs/ en la raíz del proyecto y archivo donde se guardan los eventos
RUTA_LOGS = Path(__file__).resolve().parent.parent / "logs"
ARCHIVO_LOG = RUTA_LOGS / "software_fj.log"


def _configurar_logger_base() -> logging.Logger:
    """Crea (una sola vez) el logger principal con salida a archivo."""
    base = logging.getLogger("software_fj")
    if not base.handlers:  # Evita duplicar handlers si se llama varias veces
        base.setLevel(logging.DEBUG)
        try:
            RUTA_LOGS.mkdir(parents=True, exist_ok=True)       # Crea logs/ si no existe
            handler = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        except OSError:
            # Si no se puede escribir el archivo, el sistema sigue vivo usando consola
            handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )
        base.addHandler(handler)
        base.propagate = False
    return base


def obtener_logger(modulo: str = "") -> logging.Logger:
    """Devuelve el logger del sistema o un sub-logger por módulo."""
    base = _configurar_logger_base()
    return base.getChild(modulo) if modulo else base
