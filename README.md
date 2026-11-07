# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Curso Programación (213023) – UNAD – Fase 4: Prácticas simuladas. Grupo 213023A_2204.
Proyecto en Python orientado a objetos, sin bases de datos; el único archivo
que se escribe es el log de eventos y errores (`logs/software_fj.log`).

## Estructura
- `software_fj/excepciones.py` – excepciones personalizadas.
- `software_fj/registro_logs.py` – configuración del archivo de logs.
- `software_fj/entidad_base.py` – clase abstracta de entidades generales.
- `software_fj/servicios/` – clase abstracta `Servicio` y servicios hijos.
- `demo_servicios.py` – simulación de 14 operaciones (válidas e inválidas).

## Ejecución
```
python demo_servicios.py
```

## Distribución del trabajo
| Integrante | Responsabilidad | Usuario GitHub |
|---|---|---|
| Kevin David Rojas Ibarra | Clase abstracta `Servicio` + 3 servicios hijos | (completar) |
| (Integrante 2) | Entidad abstracta + clase `Cliente` | (completar) |
| (Integrante 3) | Clase `Reserva` | (completar) |
| (Integrante 4) | Excepciones y logs / integración | (completar) |
| (Integrante 5) | `main.py` con 10+ operaciones, README y pruebas | (completar) |
