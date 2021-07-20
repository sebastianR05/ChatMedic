import requests
import json

def consultarMedicamentosByName(name):
    url = "http://localhost:5000/consultarmedicamentos/" + name
    response = requests.get(url)
    return response.json()    

def consultarMedicamentosDisponibles():
    url = "http://localhost:5000/consultarmedicamentosdisponibles"
    response = requests.get(url)
    return response.json()    

def sendEmail(asunto, mensaje, destinatario):
    url = "http://localhost:5000/enviaremail"
    json = {
        'asunto': asunto,
        'mensaje': mensaje,
        'destinatario': destinatario
    }
    response = requests.post(url, json=json)
    return response.json()   

def guardarSolicitudMedicamento(datos):
    url = "http://localhost:5000/guardarsolicitudmedicamento" 
    response = requests.post(url, json=datos)
    return response.json()  

def guardarLogEmail(datos):
    url = "http://localhost:5000/guardarlogemail" 
    response = requests.post(url, json=datos)
    return response.json()  
    