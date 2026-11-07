"""Servicio hijo 1: reserva de salas (se cobra por hora)."""

from software_fj.excepciones import ParametroInvalidoError
from software_fj.servicios.servicio import Servicio


class ReservaSala(Servicio):
    """Sala de reuniones con capacidad limitada y proyector opcional."""

    UNIDAD_DURACION = "horas"
    RECARGO_PROYECTOR_HORA = 15000.0   # Recargo por hora si la sala tiene proyector
    DURACION_MIN, DURACION_MAX = 0.5, 12.0

    def __init__(self, nombre: str, tarifa_base: float, capacidad: int,
                 tiene_proyector: bool = False, **kwargs):
        super().__init__(nombre, tarifa_base, **kwargs)   # Valida nombre y tarifa
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise ParametroInvalidoError("La capacidad debe ser un entero mayor que cero.")
        self._capacidad = capacidad
        self._tiene_proyector = bool(tiene_proyector)

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @property
    def tiene_proyector(self) -> bool:
        return self._tiene_proyector

    def validar_parametros(self, duracion, **opciones) -> None:
        # Duración: número entre 0.5 y 12 horas, en pasos de media hora
        horas = self._validar_numero_positivo(duracion, "duracion")
        if not self.DURACION_MIN <= horas <= self.DURACION_MAX or (horas * 2) % 1 != 0:
            raise ParametroInvalidoError(
                "La duración debe estar entre 0.5 y 12 horas, en múltiplos de 0.5.")
        # Opción 'asistentes': si se informa, no puede superar la capacidad
        asistentes = opciones.get("asistentes")
        if asistentes is not None:
            if isinstance(asistentes, bool) or not isinstance(asistentes, int) or asistentes <= 0:
                raise ParametroInvalidoError("Los asistentes deben ser un entero positivo.")
            if asistentes > self._capacidad:
                raise ParametroInvalidoError(
                    f"{asistentes} asistentes superan la capacidad de {self._capacidad}.")

    def calcular_costo_base(self, duracion: float) -> float:
        tarifa_hora = self.tarifa_base
        if self._tiene_proyector:
            tarifa_hora += self.RECARGO_PROYECTOR_HORA   # Suma el recargo por hora
        return tarifa_hora * duracion

    def describir(self) -> str:
        proyector = "con proyector" if self._tiene_proyector else "sin proyector"
        return (f"[Sala] {self.nombre} ({self.id}) - capacidad {self._capacidad} personas, "
                f"{proyector}, ${self.tarifa_base:,.0f} por hora.")
