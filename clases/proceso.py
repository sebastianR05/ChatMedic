import utils.mensajes as mensajes
import utils.funciones as funciones
import utils.callApi as callapi
from datetime import datetime

class Proceso:

    # Metodo inicial del proceso
    def inicio():
        repetir_captura_nombres = True
        repetir_opcion_inicial = True
        nombres = ""
        # Realiza ciclo para validar que el nombre ingresado sea carcteres y no numeros
        while repetir_captura_nombres == True:
            msj = "Buen día, por favor ingrese su nombre"
            mensajes.mostrarMensaje(msj)
            nombres = input()
            # valida si el valor inresado por el usuario no es texto, en caso que no sea letras se repite el ciclo
            if(funciones.validaNumeros(nombres)):
                repetir_captura_nombres = True
            else:
                repetir_captura_nombres = False

        # Realiza ciclo para validar que la opcion ingresada sea numerica y este dentro de las opciones validas
        while repetir_opcion_inicial == True:   
            # llama metodo para mostrar el menu principal         
            Proceso.menuPrincipal(nombres)
            opcion_inicial = input()
            # valia que la opcion ingresada por el usuario sean numeros para continuar con el proceso
            if(funciones.validaNumeros(opcion_inicial)):
                if(opcion_inicial != "1" and opcion_inicial != "2" and opcion_inicial != "3"):
                    msj = "La opción ingresada no coincide con niguna de la opciones presentadas, intente de nuevo"
                    mensajes.mostrarMensaje(msj)
                    repetir_opcion_inicial = True
                else:
                    repetir_opcion_inicial = False
                    return opcion_inicial
            else:
                repetir_opcion_inicial = True
    
    # Metodo que muestra la opciones del menu principal
    def menuPrincipal(nombres):
        msj = "\n" + nombres + ", a continuación ingrese el valor de la opción que requiera para su consulta \n"
        mensajes.mostrarMensaje(msj)
        msj = "Marque 1, para consultar la disponibilidad de medicamentos \n"
        msj += "Marque 2, para solicitar un medicamento \n"
        msj += "Marque 3, para finalizar el chat"
        mensajes.mostrarMensaje(msj)

    # Metodo que permite capturar el nombre del medicamento para asi realizar la consulta a la API
    def consultarMedicamentos():
        consulta_medicamento = True
        # Realiza ciclo para consultar medicamentos siempre y cuando el usuario decida finalizar la consulta
        while consulta_medicamento == True:
            msj = "\nPor favor ingrese el nombre del medicamento a consultar"
            mensajes.mostrarMensaje(msj)
            nombres_medicamento = input()
            # Realiza consumo de una api de consulta de medicamento por descripcion
            response = callapi.consultarMedicamentosByName(nombres_medicamento)
            # valida si la respuesta de la API es exitosa paea asi mostrar la informacion recibida del medicamento consultado
            if(response["exitoso"]):
                # valida la disponibilidad del medicamento
                if(response["disponible"]):                    
                    consulta_medicamento = False
                    Proceso.mostrarInformacionMedicamento(response)
                    consulta_medicamento = Proceso.validarNuevamenteConsulta()
                else:
                    mensajes.mostrarMensaje("\nEl medicamento no esta disponible")
                    consulta_medicamento = Proceso.validarNuevamenteConsulta()
            else:
                mensajes.mostrarMensaje(response["mensaje"])
                consulta_medicamento = Proceso.validarNuevamenteConsulta()                

    # Metodo que valida la opcion ingresada por el usuario en caso erroneo de digitacion muestra nuevamente la consulta
    def validarNuevamenteConsulta():
        repetir_opcion_consulta = True
        # Realiza ciclo para mostrar opcion de menu para la consulta de otro medicamento o finalizacion del chat hasta que el usuario lo indique
        while repetir_opcion_consulta == True:
            msj = "\nDesea consultar otro medicamento\n" 
            msj += "Marque 1 para consultar otro medicamento\n"
            msj += "Marque 2 para finalizar el chat"
            mensajes.mostrarMensaje(msj)
            opcion = input()
            # Valida si la opcion ingresada por el usuario son numeros para continuar con el proceso o finalizar el chat
            if(funciones.validaNumeros(opcion)):
                if(opcion == "1"):
                    return True
                elif(opcion == "2"):
                    Proceso.finalizacionChat()
                    return False
                else:
                    repetir_opcion_consulta = True

    # Metodo que permite mostrar al usuario la informacion del medicamento consultado
    def mostrarInformacionMedicamento(response):
        mensajes.mostrarMensaje("\nEl medicamento está disponible")
        msj = "\nMedicamento: " + response["descripcion"] 
        msj += "\nCantidad:" + str(response["cantidad"])
        msj += "\nObservación:" + response["observacion"]
        mensajes.mostrarMensaje(msj)

    # Metodo para solicitar un medicamento
    def solicitarMedicamentos():
        # Consume api para consultar los medicamentos disponibles en la base de datos y mostrarlos al usuario
        response = callapi.consultarMedicamentosDisponibles()
        # Valida si la respuesta de la api es exitosa para mostrar los medicamentos disponibles
        if(response["exitoso"]):
            # llama metodo que recibe la respuesta de la api con los medicamentos disponibles para asi mostrarlos al usuario
            Proceso.mostrarMedicamentosDisponibles(response)

    # Metodo que le muestra al usuario los medicamentos disponibles obtenidos en la respuesta de la API
    def mostrarMedicamentosDisponibles(response):
        repetir_solicitud_medicamento = True
        # Realiza ciclo para solicitar un medicamento segun disponibilidad
        while repetir_solicitud_medicamento == True:
            msj = "\nAcontinuación marque la opción del medicamento que desea solicitar\n"
            mensajes.mostrarMensaje(msj)
            contador = 1
            # Realiza cliclo sobre los medicamentos disponibles y los muestra al usuario
            for data in response["data"]:
                msj = "Marque " + str(contador) + " para solicitar " + data["descripcion"]
                mensajes.mostrarMensaje(msj)
                contador = contador + 1
            opcion = input()
            # Valida la opcion del medicamento escogido por el usuario sea un numero segun el listado mostrado
            if(funciones.validaNumeros(opcion)):
                # valida la opcion ingresada exista o coincida con un medicamento
                if(int(opcion) > len(response["data"])):
                    repetir_solicitud_medicamento = True
                else:
                    if(int(opcion) != 0):
                        repetir_solicitud_medicamento = False
                        # Llama metodo para la captura de los datos personales para finalizar la solicitud
                        Proceso.capturarDatosSolicitudMedicamento(response["data"], int(opcion))
                    else:
                        repetir_solicitud_medicamento = True
            else:
                repetir_solicitud_medicamento = True

    # Metodo que permite la captura de los datos personales del usuario para crear la solicitud y el envio de correo
    def capturarDatosSolicitudMedicamento(opciones_medicamento, opcion_escogida):
        contador = 1
        medicamento_seleccionado = ""
        # realiza ciclo for para iterar las opciones de medicamento y asi recuperar el medicamento escogido por el usuario
        for data in opciones_medicamento:
            if(opcion_escogida == contador):
                medicamento_seleccionado = data["descripcion"]
                break
            contador = contador + 1

        # Captura de datos
        msj = "\nPara finalizar con la solicitud por favor ingrese los siguientes datos\n"
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

        msj = "\nEstamos procesando su solicitud, espere un momento...\n"
        mensajes.mostrarMensaje(msj)

        # instancia en una variable la fecha actual del sistema
        fecha_actual = str(datetime.now())
        asunto = "Solicitud Medicamento"

        msj = "Senor(a) " + nombres.upper() + ","
        msj += " usted ha solicitado el envio del medicamento " + medicamento_seleccionado
        msj += ", a la direccion " + direccion + " acorde a la solicitud realizada"
        
        # crear el objeto json con el request para crear la solicitud del medicamento
        datos = {
            "nombres": nombres.upper(),
            "identificacion": identificacion,
            "telefono": telefono,
            "direccion": direccion,
            "email": email,
            "fecha_solicitud": fecha_actual,
            "medicamento": medicamento_seleccionado
        }

        # crea el objeto json con el request para crear el log del email
        datos_log = {
            "asunto": asunto,
            "mensaje": msj,
            "destinatario": email,
        }

        # hace llamado de la api para crear la solicitud del medicamento
        result = callapi.guardarSolicitudMedicamento(datos)

        # valida si la respuesta de la api de crear solicitud se hizo correctamente 
        if(result["exitoso"]):
            # muestra mensaje de la creacion de la solicitud correctamente
            mensajes.mostrarMensaje(result["mensaje"])
            # hace llamado de la api para el envio del email con la notificacion de la solicitud
            response = callapi.sendEmail(asunto, msj, email) 
            # valida si la api del envio de email fu exitoso
            if(response["exitoso"]):  
                # hace llamado de la api para guardar el log del email
                callapi.guardarLogEmail(datos_log)
                # llama metodo para finalizar el chat
                Proceso.finalizacionChat()
        else:
            mensajes.mostrarMensaje(result["mensaje"])
            Proceso.finalizacionChat()

    # Metodo que muestra mensaje de finalizacion del chat   
    def finalizacionChat():
        msj = "\nHa finalizado el chat. Buen día"
        mensajes.mostrarMensaje(msj)