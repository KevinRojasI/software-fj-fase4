from software_fj.entidad_base import EntidadBase

class Cliente(EntidadBase):
    """
    Clase Cliente que hereda de EntidadBase.
    Implementa la validación de datos usando excepciones para garantizar robustez.
    """
    
    def __init__(self, nombre: str, correo: str, identificador: str | None = None):
        # Pasamos el identificador a la clase padre
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        
        # Llamamos a nuestro método de validación
        self.validar_datos()

    def validar_datos(self):
        """
        Valida que los datos del cliente sean correctos. 
        Si hay un error, lanza una excepción ValueError.
        """
        if not self.nombre or self.nombre.strip() == "":
            raise ValueError("Error: El nombre del cliente es obligatorio.")
            
        # Validación básica de correo
        if not self.correo or "@" not in self.correo or "." not in self.correo:
            raise ValueError(f"Error: El correo '{self.correo}' no tiene un formato válido.")

    def describir(self) -> str:
        """
        Implementación del método abstracto 'describir' exigido por EntidadBase.
        """
        return f"Cliente [ID: {self.id}] - Nombre: {self.nombre} - Correo: {self.correo}"
