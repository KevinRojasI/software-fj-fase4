from abc import ABC, abstractmethod
import itertools

class EntidadBase(ABC):
    """
    Clase abstracta que representa las entidades generales del sistema.
    Versión final implementada por el Integrante 2.
    """
    
    # Generador de consecutivos para ids automáticos (ENT-0001, ENT-0002...)
    _contador = itertools.count(1)

    def __init__(self, identificador: str | None = None):
        # Si no se entrega id, se genera uno automático
        self._id = identificador or f"ENT-{next(EntidadBase._contador):04d}"

    @property
    def id(self) -> str:
        """Identificador de solo lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Obliga a las clases hijas a saber describirse (Método de Kevin)."""
        pass
        
    @abstractmethod
    def validar_datos(self) -> None:
        """Obliga a las clases hijas a validar sus propios datos (Tu aporte)."""
        pass
