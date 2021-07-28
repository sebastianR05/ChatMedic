import clases.proceso as proceso

# Llama metodo de incio de la clase proceso para inciar la interacion con el usuario
opcion_inicio = proceso.Proceso.inicio()

# Valida la opcion ingresada por el usuario para continuar con el proceso
if(opcion_inicio == "1"):
    # Llama metodo para la consulta de medicamentos
    proceso.Proceso.consultarMedicamentos()
elif(opcion_inicio == "2"):
    # Llama metodo para la solicitud de medicamentos
    proceso.Proceso.solicitarMedicamentos()
elif(opcion_inicio == "3"):
    # Llama metodo para la finalizacion del chat con el usuario
    proceso.Proceso.finalizacionChat()