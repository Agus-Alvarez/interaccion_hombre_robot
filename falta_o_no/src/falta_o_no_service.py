from naoqi import ALModule, ALProxy

from naoqi import ALModule, ALProxy

class FaltaONoService(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.tabletService = ALProxy("ALTabletService")
        self.dialog = ALProxy("ALDialog")
        self.imagenes = [] 
        self.indice_imagen_actual = 0
        self.nombre_topico = "falta_o_no_topico" 

    def iniciar_juego(self):
        self.indice_imagen_actual = 0
        self.cargar_imagenes() # Método para cargar la lista de imágenes
        if self.imagenes:
            self.mostrar_imagen()
            self.dialog.activateTopic(self.nombre_topico)
            self.dialog.subscribe(self.getName())
        else:
            self.dialog.say("No hay imágenes disponibles para el juego.")

    def cargar_imagenes(self):
        # Lista de imágenes con su información:
        # "archivo": nombre del archivo de imagen en la carpeta 'html'
        # "es_falta": True si es falta, False si no lo es
        # "regla": Explicación o regla asociada a la jugada
        self.imagenes = [
            {"archivo": "entrada limpia.jpg", "es_falta": False, "regla": "Una entrada limpia al balón para ganar posesión no es falta."},
            {"archivo": "mano.jpeg", "es_falta": True, "regla": "Tocar el balón deliberadamente con la mano es falta."},
            {"archivo": "patada.jpg", "es_falta": True, "regla": "Dar una patada a un oponente es falta."},
            {"archivo": "patadados.jpeg", "es_falta": True, "regla": "Dar una patada a un oponente es falta."},
        ]

    def mostrar_imagen(self):
        if 0 <= self.indice_imagen_actual < len(self.imagenes):
            ruta_imagen = "http://127.0.0.1/apps/falta_o_no/html/" + self.imagenes[self.indice_imagen_actual]["archivo"]
            self.tabletService.showWebview(ruta_imagen)
            self.dialog.say("Mira la imagen en la tableta. ¿Es falta o no?")
        else:
            self.dialog.say("¡Hemos visto todas las jugadas!")
            self.finalizar_juego()

    def verificar_respuesta(self, respuesta):
        if not self.imagenes:
            self.dialog.say("El juego no ha comenzado o no hay imágenes.")
            return

        respuesta_usuario = respuesta.lower()
        es_falta_correcta = self.imagenes[self.indice_imagen_actual]["es_falta"]
        regla = self.imagenes[self.indice_imagen_actual]["regla"]
        self.indice_imagen_actual += 1

        if (respuesta_usuario == "falta" and es_falta_correcta) or (respuesta_usuario == "no falta" and not es_falta_correcta):
            self.dialog.say("¡Correcto! " + regla)
            self.mostrar_imagen()
        else:
            self.dialog.say("Incorrecto. " + regla)
            self.mostrar_imagen()

    def finalizar_juego(self):
        self.dialog.unsubscribe(self.getName())
        self.dialog.deactivateTopic(self.nombre_topico)

    def main(session):
        global module
        module = FaltaONoService("FaltaONoService")

    if __name__ == "__main__":
        from naoqi import ALBroker
        myBroker = ALBroker("myBroker", "0.0.0.0", 0, "127.0.0.1", 9559)
        main(myBroker.getSession())