"""Servicio hijo 2: alquiler de equipos (se cobra por día)."""

from software_fj.excepciones import ParametroInvalidoError
from software_fj.servicios.servicio import Servicio


class AlquilerEquipo(Servicio):
    """Equipo tecnológico alquilado por días, con descuento semanal."""

    UNIDAD_DURACION = "días"
    DIAS_MAX = 30
    DIAS_PARA_DESCUENTO = 7
    DESCUENTO_SEMANAL = 0.10   # 10 % menos si se alquila 7 días o más

    def __init__(self, nombre: str, tarifa_base: float, tipo_equipo: str,
                 deposito_garantia: float = 0.0, **kwargs):
        super().__init__(nombre, tarifa_base, **kwargs)   # Valida nombre y tarifa
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ParametroInvalidoError("El tipo de equipo es obligatorio.")
        if (isinstance(deposito_garantia, bool)
                or not isinstance(deposito_garantia, (int, float))
                or deposito_garantia < 0):
            raise ParametroInvalidoError("El depósito debe ser un número mayor o igual a 0.")
        self._tipo_equipo = tipo_equipo.strip()
        self._deposito_garantia = float(deposito_garantia)

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @property
    def deposito_garantia(self) -> float:
        return self._deposito_garantia

    def validar_parametros(self, duracion, **opciones) -> None:
        # Los equipos se alquilan por días completos (enteros)
        if isinstance(duracion, bool) or not isinstance(duracion, int):
            raise ParametroInvalidoError("Los días de alquiler deben ser un número entero.")
        if not 1 <= duracion <= self.DIAS_MAX:
            raise ParametroInvalidoError(
                f"El alquiler debe ser de 1 a {self.DIAS_MAX} días.")

    def calcular_costo_base(self, duracion: float) -> float:
        costo = self.tarifa_base * duracion
        if duracion >= self.DIAS_PARA_DESCUENTO:
            costo *= (1 - self.DESCUENTO_SEMANAL)   # Descuento por alquiler largo
        return costo

    def describir(self) -> str:
        return (f"[Equipo] {self.nombre} ({self.id}) - tipo {self._tipo_equipo}, "
                f"${self.tarifa_base:,.0f} por día, depósito reembolsable "
                f"${self._deposito_garantia:,.0f}.")
