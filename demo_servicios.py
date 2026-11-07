"""Demostración de la parte de Kevin David Rojas Ibarra:
clase abstracta Servicio y servicios hijos (sala, equipo y asesoría).

Ejecutar:  python demo_servicios.py
Simula 14 operaciones (válidas e inválidas) sin que el programa se detenga.
"""

from software_fj.excepciones import ErrorSoftwareFJ
from software_fj.registro_logs import obtener_logger
from software_fj.servicios import (
    AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio,
)

logger = obtener_logger("demo")


def ejecutar_operacion(numero: int, descripcion: str, accion):
    """Ejecuta una operación con try/except/else/finally sin detener el programa."""
    print(f"\n--- Operación {numero}: {descripcion}")
    try:
        resultado = accion()                       # Se intenta la operación
    except ErrorSoftwareFJ as error:               # Error controlado del dominio
        logger.error("Operación %d falló: %s", numero, error)
        print(f"   ERROR CONTROLADO -> {error}")
        return None
    except Exception as error:                     # Cualquier otro error inesperado
        logger.critical("Operación %d error inesperado: %r", numero, error)
        print(f"   ERROR INESPERADO -> {type(error).__name__}: {error}")
        return None
    else:                                          # Solo si no hubo errores
        logger.info("Operación %d exitosa.", numero)
        print(f"   OK -> {resultado}")
        return resultado
    finally:                                       # Siempre se ejecuta
        print(f"   (operación {numero} finalizada)")


def main() -> None:
    logger.info("===== Inicio de la demostración de servicios =====")

    sala = ejecutar_operacion(1, "Crear sala válida",
        lambda: ReservaSala("Sala Innovación", 80000, capacidad=10, tiene_proyector=True))
    ejecutar_operacion(2, "Crear sala con capacidad negativa (inválida)",
        lambda: ReservaSala("Sala Rota", 80000, capacidad=-5))
    equipo = ejecutar_operacion(3, "Crear alquiler de equipo válido",
        lambda: AlquilerEquipo("Portátil Gamer", 45000, "Portátil", deposito_garantia=500000))
    ejecutar_operacion(4, "Crear equipo con tarifa en texto (inválida)",
        lambda: AlquilerEquipo("Cámara 4K", "gratis", "Cámara"))
    asesoria = ejecutar_operacion(5, "Crear asesoría válida",
        lambda: AsesoriaEspecializada("Asesoría Python", 60000, "Programación", "senior"))
    ejecutar_operacion(6, "Crear asesoría con nivel inexistente",
        lambda: AsesoriaEspecializada("Asesoría X", 60000, "Redes", "maestro"))
    ejecutar_operacion(7, "Instanciar la clase abstracta Servicio",
        lambda: Servicio("Servicio genérico", 1000))

    if sala:
        ejecutar_operacion(8, "Costo sala 3 h con IVA 19 %",
            lambda: sala.calcular_costo_con_impuesto(3))
        ejecutar_operacion(9, "Sala con 25 asistentes (supera capacidad 10)",
            lambda: sala.calcular_costo(2, asistentes=25))
    if equipo:
        ejecutar_operacion(10, "Equipo 10 días con 5 % de descuento + IVA",
            lambda: equipo.calcular_costo_con_descuento(10, 0.05, impuesto=0.19))
        ejecutar_operacion(11, "Equipo con días = None (parámetro faltante)",
            lambda: equipo.calcular_costo(None))
    if asesoria:
        ejecutar_operacion(12, "Asesoría 2.5 h sin impuesto",
            lambda: asesoria.calcular_costo(2.5))
        ejecutar_operacion(13, "Asesoría con descuento imposible (150 %)",
            lambda: asesoria.calcular_costo(2, descuento=1.5))
        asesoria.marcar_no_disponible()
        ejecutar_operacion(14, "Cotizar asesoría NO disponible",
            lambda: asesoria.calcular_costo(2))
        asesoria.marcar_disponible()

    # Polimorfismo: misma llamada, comportamiento distinto según el servicio
    print("\n=== Polimorfismo: describir() en cada servicio ===")
    for servicio in (sala, equipo, asesoria):
        if servicio:
            print(servicio.describir())

    logger.info("===== Fin de la demostración de servicios =====")
    print("\nDemostración terminada. Revise logs/software_fj.log")


if __name__ == "__main__":
    main()
