from utils.mensajes import mostrarMensaje
import conexion as conecction
import clases.proceso as proceso
import utils.mensajes as mensajes

opcion_inicio = proceso.Proceso.inicio()
if(opcion_inicio == "1"):
    proceso.Proceso.consultarMedicamentos()
elif(opcion_inicio == "2"):
    proceso.Proceso.solicitarMedicamentos()