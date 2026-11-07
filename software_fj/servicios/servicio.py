"""Clase abstracta Servicio: base de todos los servicios de Software FJ."""

import math
from abc import ABC, abstractmethod
from numbers import Real

from software_fj.entidad_base import EntidadBase
from software_fj.excepciones import (
    CalculoInconsistenteError,
    ErrorSoftwareFJ,
    ParametroInvalidoError,
    ServicioNoDisponibleError,
)
from software_fj.registro_logs import obtener_logger

logger = obtener_logger("servicios")  # Todos los eventos de servicios van al log


class Servicio(EntidadBase, ABC):
    """Servicio genérico. Las clases hijas implementan los métodos abstractos."""

    IVA_POR_DEFECTO = 0.19      # IVA del 19 % usado por las variantes con impuesto
    UNIDAD_DURACION = "horas"   # Las hijas pueden cambiarla (p. ej. "días")

    def __init__(self, nombre: str, tarifa_base: float,
                 disponible: bool = True, identificador: str | None = None):
        super().__init__(identificador)          # Inicializa el id de EntidadBase
        self.nombre = nombre                     # Pasa por el setter con validación
        self.tarifa_base = tarifa_base           # Pasa por el setter con validación
        self._disponible = bool(disponible)      # Estado de disponibilidad (privado)

    # ------------------------------------------------------------------
    # Encapsulación: propiedades con validación estricta
    # ------------------------------------------------------------------
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ParametroInvalidoError(
                "El nombre del servicio debe ser texto de al menos 3 caracteres.")
        self._nombre = valor.strip()             # Se guarda sin espacios sobrantes

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        self._tarifa_base = self._validar_numero_positivo(valor, "tarifa_base")

    @property
    def disponible(self) -> bool:
        return self._disponible

    def marcar_disponible(self) -> None:
        self._disponible = True
        logger.info("Servicio %s marcado como disponible.", self.id)

    def marcar_no_disponible(self) -> None:
        self._disponible = False
        logger.info("Servicio %s marcado como NO disponible.", self.id)

    # ------------------------------------------------------------------
    # Utilidades de validación reutilizables por las clases hijas
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_numero_positivo(valor, campo: str) -> float:
        """Verifica que ``valor`` sea un número real, finito y mayor que cero."""
        if isinstance(valor, bool) or not isinstance(valor, Real):
            raise ParametroInvalidoError(
                f"'{campo}' debe ser numérico; se recibió {type(valor).__name__}.")
        if not math.isfinite(valor) or valor <= 0:
            raise ParametroInvalidoError(f"'{campo}' debe ser un número mayor que cero.")
        return float(valor)

    @staticmethod
    def _validar_porcentaje(valor, campo: str, maximo: float) -> float:
        """Verifica que ``valor`` sea un número entre 0 y ``maximo``."""
        if isinstance(valor, bool) or not isinstance(valor, Real) or not math.isfinite(valor):
            raise ParametroInvalidoError(f"'{campo}' debe ser un número válido.")
        if not 0 <= valor <= maximo:
            raise ParametroInvalidoError(f"'{campo}' debe estar entre 0 y {maximo}.")
        return float(valor)

    def verificar_disponibilidad(self) -> None:
        """Lanza ServicioNoDisponibleError si el servicio no se puede usar."""
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' ({self.id}) no está disponible.")

    # ------------------------------------------------------------------
    # Métodos abstractos: cada servicio hijo los sobrescribe (polimorfismo)
    # ------------------------------------------------------------------
    @abstractmethod
    def calcular_costo_base(self, duracion: float) -> float:
        """Costo sin impuestos ni descuentos, según las reglas del servicio."""

    @abstractmethod
    def validar_parametros(self, duracion, **opciones) -> None:
        """Valida duración y opciones propias; lanza ParametroInvalidoError."""

    @abstractmethod
    def describir(self) -> str:
        """Descripción legible del servicio."""

    # ------------------------------------------------------------------
    # Métodos sobrecargados (variantes del cálculo de costos)
    # ------------------------------------------------------------------
    def calcular_costo(self, duracion, impuesto: float = 0.0,
                       descuento: float = 0.0, **opciones) -> float:
        """Costo total = base * (1 - descuento) * (1 + impuesto).

        Python no tiene sobrecarga nativa; se simula con parámetros opcionales
        y con las variantes ``calcular_costo_con_impuesto`` y
        ``calcular_costo_con_descuento``.
        """
        try:
            self.verificar_disponibilidad()                          # ¿Está disponible?
            self.validar_parametros(duracion, **opciones)            # Reglas de la hija
            impuesto = self._validar_porcentaje(impuesto, "impuesto", 1.0)
            descuento = self._validar_porcentaje(descuento, "descuento", 0.9)
            costo_base = self.calcular_costo_base(duracion)          # Polimorfismo
            total = costo_base * (1 - descuento) * (1 + impuesto)    # Fórmula final
            if total <= 0 or not math.isfinite(total):
                raise CalculoInconsistenteError(
                    f"El cálculo produjo un total inválido ({total}).")
        except ErrorSoftwareFJ as error:
            # Error propio del dominio: se registra y se propaga sin perder el tipo
            logger.warning("Cálculo rechazado en %s: %s", self.id, error)
            raise
        except (TypeError, ValueError, ArithmeticError) as error:
            # Error inesperado: se encadena (from) a una excepción propia
            logger.error("Error inesperado calculando %s: %r", self.id, error)
            raise CalculoInconsistenteError(
                "No fue posible calcular el costo con los datos entregados.") from error
        else:
            # Solo se ejecuta si NO hubo excepciones
            logger.info("Costo calculado para %s: %.2f", self.id, total)
            return round(total, 2)
        finally:
            # Se ejecuta siempre, haya o no error
            logger.debug("Fin del cálculo de costo para %s", self.id)

    def calcular_costo_con_impuesto(self, duracion, impuesto: float | None = None,
                                    **opciones) -> float:
        """Variante: aplica solo impuesto (IVA por defecto si no se indica)."""
        tasa = self.IVA_POR_DEFECTO if impuesto is None else impuesto
        return self.calcular_costo(duracion, impuesto=tasa, **opciones)

    def calcular_costo_con_descuento(self, duracion, descuento: float,
                                     impuesto: float = 0.0, **opciones) -> float:
        """Variante: aplica descuento y, opcionalmente, impuesto."""
        return self.calcular_costo(duracion, impuesto=impuesto,
                                   descuento=descuento, **opciones)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.id!r}, nombre={self.nombre!r})"
