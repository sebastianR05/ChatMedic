# Metodo que recibe un valor y retorna verdadero si es numero y falso si es diferente
def validaNumeros(valor):
    if(valor.isdigit()):
        return True
    else:
        return False

# Metodo que recibe un texto y lo convierte en mayuscula y lo retorna
def convertMayuscula(texto):
    return texto.upper()