"""Servicio hijo 3: asesorías especializadas (se cobra por hora y nivel)."""

from software_fj.excepciones import ParametroInvalidoError
from software_fj.servicios.servicio import Servicio


class AsesoriaEspecializada(Servicio):
    """Asesoría de un especialista; el nivel del asesor modifica la tarifa."""

    UNIDAD_DURACION = "horas"
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}   # Multiplicador por nivel
    DURACION_MIN, DURACION_MAX = 1.0, 8.0

    def __init__(self, nombre: str, tarifa_base: float, especialidad: str,
                 nivel: str = "junior", **kwargs):
        super().__init__(nombre, tarifa_base, **kwargs)   # Valida nombre y tarifa
        if not isinstance(especialidad, str) or len(especialidad.strip()) < 3:
            raise ParametroInvalidoError("La especialidad debe tener al menos 3 caracteres.")
        if not isinstance(nivel, str) or nivel.strip().lower() not in self.NIVELES:
            raise ParametroInvalidoError(
                f"Nivel inválido. Opciones: {', '.join(self.NIVELES)}.")
        self._especialidad = especialidad.strip()
        self._nivel = nivel.strip().lower()

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @property
    def nivel(self) -> str:
        return self._nivel

    def validar_parametros(self, duracion, **opciones) -> None:
        # Entre 1 y 8 horas, en pasos de media hora
        horas = self._validar_numero_positivo(duracion, "duracion")
        if not self.DURACION_MIN <= horas <= self.DURACION_MAX or (horas * 2) % 1 != 0:
            raise ParametroInvalidoError(
                "La asesoría debe durar entre 1 y 8 horas, en múltiplos de 0.5.")

    def calcular_costo_base(self, duracion: float) -> float:
        return self.tarifa_base * self.NIVELES[self._nivel] * duracion

    def describir(self) -> str:
        return (f"[Asesoría] {self.nombre} ({self.id}) - {self._especialidad}, "
                f"nivel {self._nivel}, ${self.tarifa_base:,.0f} por hora base.")
