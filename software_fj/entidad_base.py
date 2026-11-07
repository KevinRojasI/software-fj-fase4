"""Clase abstracta que representa las entidades generales del sistema.

NOTA DE EQUIPO: esta versión es PROVISIONAL para que la clase Servicio pueda
ejecutarse de forma independiente. El compañero responsable de la entidad
abstracta general puede reemplazarla; Servicio solo necesita ``id`` y
``describir()``.
"""

import itertools
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Entidad general: todo objeto del sistema tiene un id y se puede describir."""

    _contador = itertools.count(1)  # Generador de consecutivos para ids automáticos

    def __init__(self, identificador: str | None = None):
        # Si no se entrega id, se genera uno consecutivo (ENT-0001, ENT-0002, ...)
        self._id = identificador or f"ENT-{next(EntidadBase._contador):04d}"

    @property
    def id(self) -> str:
        """Identificador de solo lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad concreta debe saber describirse."""

    def __str__(self) -> str:
        return self.describir()
