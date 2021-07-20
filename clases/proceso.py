import utils.mensajes as mensajes
import utils.funciones as funciones
import utils.callApi as callapi
from datetime import datetime

class Proceso:

    def inicio():
        repetir_captura_nombres = True
        repetir_opcion_inicial = True
        nombres = ""
        # Realiza ciclo para validar que el nombre ingresado sea carcteres y no numeros
        while repetir_captura_nombres == True:
            msj = "Buen día, por favor ingrese su nombre"
            mensajes.mostrarMensaje(msj)
            nombres = input()
            if(funciones.validaNumeros(nombres)):
                repetir_captura_nombres = True
            else:
                repetir_captura_nombres = False

        # Realiza ciclo para validar que la opcion ingresada sea numerica y este dentro de las opciones validas
        while repetir_opcion_inicial == True:
            msj = nombres + ", a continuación ingrese el valor de la opción que requiera para su consulta \n"
            mensajes.mostrarMensaje(msj)
            msj = "Marque 1, para consultar la disponibilidad de medicamentos \n"
            msj += "Marque 2, para solicitar un medicamento \n"
            mensajes.mostrarMensaje(msj)
            opcion_inicial = input()
            if(funciones.validaNumeros(opcion_inicial)):
                if(opcion_inicial != "1" and opcion_inicial != "2"):
                    msj = "La opción ingresada no coincide con niguna de la opciones presentadas, intente de nuevo"
                    mensajes.mostrarMensaje(msj)
                    repetir_opcion_inicial = True
                else:
                    repetir_opcion_inicial = False
                    return opcion_inicial
            else:
                repetir_opcion_inicial = True
    
    def consultarMedicamentos():
        consulta_medicamento = True
        while consulta_medicamento == True:
            msj = "Por favor ingrese el nombre del medicamento a consultar"
            mensajes.mostrarMensaje(msj)
            nombres_medicamento = input()
            response = callapi.consultarMedicamentosByName(nombres_medicamento)
            if(response["exitoso"]):
                # valida la disponibilidad del medicamento
                if(response["disponible"]):                    
                    consulta_medicamento = False
                    Proceso.mostrarInformacionMedicamento(response)
                else:
                    mensajes.mostrarMensaje("El medicamento no esta disponible")
                    consulta_medicamento = Proceso.validarNuevamenteConsulta()
            else:
                mensajes.mostrarMensaje(response["mensaje"])
                consulta_medicamento = Proceso.validarNuevamenteConsulta()                

    def validarNuevamenteConsulta():
        repetir_opcion_consulta = True
        while repetir_opcion_consulta == True:
            msj = "Desea consultar otro medicamento\n" 
            msj += "Marque 1 para consultar otro medicamento\n"
            msj += "Marque 2 para finalizar el chat"
            mensajes.mostrarMensaje(msj)
            opcion = input()
            if(funciones.validaNumeros(opcion)):
                if(opcion == "1"):
                    return True
                elif(opcion == "2"):
                    return False
                else:
                    repetir_opcion_consulta = True

    def mostrarInformacionMedicamento(response):
        mensajes.mostrarMensaje("El medicamento está disponible")
        msj = "\nMedicamento: " + response["descripcion"] 
        msj += "\nCantidad:" + str(response["cantidad"])
        msj += "\nObservación:" + response["observacion"]
        mensajes.mostrarMensaje(msj)

    def solicitarMedicamentos():
        response = callapi.consultarMedicamentosDisponibles()
        if(response["exitoso"]):
            Proceso.mostrarMedicamentosDisponibles(response)

    def mostrarMedicamentosDisponibles(response):
        repetir_solicitud_medicamento = True
        while repetir_solicitud_medicamento == True:
            msj = "Acontinuación marque la opción del medicamento que desea solicitar\n"
            mensajes.mostrarMensaje(msj)
            contador = 1
            for data in response["data"]:
                msj = "Marque " + str(contador) + " para solicitar " + data["descripcion"]
                mensajes.mostrarMensaje(msj)
                contador = contador + 1
            opcion = input()
            if(funciones.validaNumeros(opcion)):
                repetir_solicitud_medicamento = False
                Proceso.capturarDatosSolicitudMedicamento(response["data"], int(opcion))
            else:
                repetir_solicitud_medicamento = True

    def capturarDatosSolicitudMedicamento(opciones_medicamento, opcion_escogida):
        contador = 1
        medicamento_seleccionado = ""
        for data in opciones_medicamento:
            if(opcion_escogida == contador):
                medicamento_seleccionado = data["descripcion"]
                break
            contador = contador + 1

        msj = "Para finalizar con la solicitud por favor ingrese los siguientes datos\n"
        mensajes.mostrarMensaje(msj)

        msj = "Por ingrese nombres y apellidos \n"
        mensajes.mostrarMensaje(msj)
        nombres = input()

        msj = "Por ingrese el número de identificación \n"
        mensajes.mostrarMensaje(msj)
        identificacion = input()

        msj = "Por ingrese el número de telefono o celular de contacto \n"
        mensajes.mostrarMensaje(msj)
        telefono = input()

        msj = "Por ingrese la dirección de residencia \n"
        mensajes.mostrarMensaje(msj)
        direccion = input()

        msj = "Por ingrese el email o correo electronico \n"
        mensajes.mostrarMensaje(msj)
        email = input()

        fecha_actual = str(datetime.now())
        asunto = "Solicitud Medicamento"

        msj = "Senor(a) " + nombres.upper() + ","
        msj += " usted ha solicitado el envio del medicamento " + medicamento_seleccionado
        msj += ", a la direccion " + direccion + " acorde a la solicitud realizada"
        
        datos = {
            "nombres": nombres.upper(),
            "identificacion": identificacion,
            "telefono": telefono,
            "direccion": direccion,
            "email": email,
            "fecha_solicitud": fecha_actual,
            "medicamento": medicamento_seleccionado
        }

        datos_log = {
            "asunto": asunto,
            "mensaje": msj,
            "destinatario": email,
        }

        result = callapi.guardarSolicitudMedicamento(datos)

        if(result["exitoso"]):
            mensajes.mostrarMensaje(result["mensaje"])
            response = callapi.sendEmail(asunto, msj, email) 
            if(response["exitoso"]):  
                callapi.guardarLogEmail(datos_log)
                mensajes.mostrarMensaje(response["mensaje"])  
        else:
            mensajes.mostrarMensaje(result["mensaje"])
        # if(response["exitoso"]):
        #     mensajes.mostrarMensaje(response["mensaje"])
        # else:
        #     mensajes.mostrarMensaje("No se pudo enviar el email")

