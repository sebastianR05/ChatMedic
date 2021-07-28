import requests
import json

# Metodo que consume api para la consulta de medicamento recibiendo parametro de la descripcion
def consultarMedicamentosByName(name):
    url = "http://localhost:5000/consultarmedicamentos/" + name
    response = requests.get(url)
    return response.json()    

# Metodo que consume api para la consulta de los medicamentos disponibles
def consultarMedicamentosDisponibles():
    url = "http://localhost:5000/consultarmedicamentosdisponibles"
    response = requests.get(url)
    return response.json()    

# Metodo que consume api para el envio de correos electronicos
def sendEmail(asunto, mensaje, destinatario):
    url = "http://localhost:5000/enviaremail"
    json = {
        'asunto': asunto,
        'mensaje': mensaje,
        'destinatario': destinatario
    }
    response = requests.post(url, json=json)
    return response.json()   


# Metodo que consume api para crear la solicitud de medicamento
def guardarSolicitudMedicamento(datos):
    url = "http://localhost:5000/guardarsolicitudmedicamento" 
    response = requests.post(url, json=datos)
    return response.json()  

# Metodo que consume api para almacenar el log de los email enviados
def guardarLogEmail(datos):
    url = "http://localhost:5000/guardarlogemail" 
    response = requests.post(url, json=datos)
    return response.json()  
    