#_______________________________________________________ESTACIONAMIENTO DE VEHÍCULOS_____________________________________________________

#________________________________________________________________MÓDULOS_________________________________________________________________
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import webbrowser
import pickle
import time
import os
import json
#_________________________________________________________FUNCIONES ADICIONALES__________________________________________________________
#Función: página principal
#Entradas: N/A
#Salidas: llama la función limpiar ventana y despliega la "página principal"
def mostrar_pagina_inicio():
    limpiar_ventana()
    mensaje = Label(root, text="Bienvenido al estacionamiento de vehículo, por favor seleccione una opción.", font=("Times New Roman", 14)).place(x=10, y=10)

#Función: limpiar ventana
#Entradas: N/A
#Salidas: limpia la ventana para poder desplegar diferentes funcionalidades
def limpiar_ventana():
    for widget in root.winfo_children():
        widget.place_forget()

#Función: aceptar configuraciones
#Entradas: las configuraciones elegidas por el usuario
#Salidas: registra los datos
def aceptar_configuraciones():
    global diccionario_configuracion, tipos_monedas, tipos_billetes, existe_configuracion

    verificar_monedas([int(moneda1.get()), int(moneda2.get()), int(moneda3.get())])

    verificar_billetes([int(billete1.get()), int(billete2.get()), int(billete3.get()), int(billete4.get()), int(billete5.get())])


    diccionario_configuracion = {"cantidad_espacios": int(cantidad_espacios.get()), "precio_por_hora": int(precio_por_hora.get()), "pago_minimo": int(pago_minimo.get()),
        "redondear_minuto": int(redondear_minuto.get()), "minutos_maximos_salir": int(minutos_maximos_salir.get()), "moneda1": int(moneda1.get()),
        "moneda2": int(moneda2.get()), "moneda3": int(moneda3.get()), "billete1": int(billete1.get()), "billete2": int(billete2.get()),
        "billete3": int(billete3.get()), "billete4": int(billete4.get()), "billete5": int(billete5.get()), "valor": True}

    tipos_monedas = {"moneda1": int(moneda1.get()), "moneda2": int(moneda2.get()), "moneda3": int(moneda3.get())}
    tipos_billetes = {"billete1": int(billete1.get()), "billete2": int(billete2.get()), "billete3": int(billete3.get()), "billete4": int(billete4.get()), "billete5": int(billete5.get())}
    
    for space in range(diccionario_configuracion["cantidad_espacios"]):
        parqueo.append([])

    mostrar_pagina_inicio()
    existe_configuracion = True

#Función: agregar carga al cajero
#Entradas: cantidad de dinero cargado
#Salidas: adición del dinero cargado y vuelve a función principal 
def agregar_carga():
    global cantidades_monedas
    global cantidades_billetes
    cantidades_monedas["moneda1"] += int(carga_moneda1.get())
    cantidades_monedas["moneda2"] += int(carga_moneda2.get())
    cantidades_monedas["moneda3"] += int(carga_moneda3.get())
    cantidades_billetes["billete1"] += int(carga_billete1.get())
    cantidades_billetes["billete2"] += int(carga_billete2.get())
    cantidades_billetes["billete3"] += int(carga_billete3.get())
    cantidades_billetes["billete4"] += int(carga_billete4.get())
    cantidades_billetes["billete5"] += int(carga_billete5.get())

    carga_moneda1.set(0)
    carga_moneda2.set(0)
    carga_moneda3.set(0)
    carga_billete1.set(0)
    carga_billete2.set(0)
    carga_billete3.set(0)
    carga_billete4.set(0)
    carga_billete5.set(0)

    mostrar_pagina_inicio()

#Función: mensaje error modificar parqueo por uso
#Entradas: N/A
#Salidas: ventana que indica que no se puede modificar el parqueo
def error_modificar_configuracion():
    error_modificar = Toplevel(root)
    error_modificar.title("ERROR")
    error_modificar.geometry("450x100")
    
    mensaje_modificar = Label(error_modificar, text="ERROR: no se puede modificar configuración porque el parqueo está en uso.").place(x=20, y=10)
    
    button = Button(error_modificar, text="Volver", command=error_modificar.destroy).place(x=205, y=50)

#Función: mensaje error parqueo lleno
#Entradas: N/A
#Salidas: ventana que indica que el abastecimiento del parqueo está lleno y por lo tanto no pueden ingresar más vehículos
def error_parqueo_lleno():
    error_lleno = Toplevel(root)
    error_lleno.title("ERROR")
    error_lleno.geometry("730x100")
    
    mensaje_lleno = Label(error_lleno, text="ERROR: el parqueo esta con el abastecimiento al máximo, no pueden entrar más vehículos.", font=("Arial", 12, "bold"), fg="red").place(x=20, y=10)
    
    button = Button(error_lleno, text="Volver", command=error_lleno.destroy).place(x=205, y=50)

#Función: mensaje error no existe configuración
#Entradas: N/A
#Salidas: ventana que indica que la configuración aun no ha sido registrada, y por lo tanto no se pueden acceder a ciertas funcionalidades del parqueo
def error_no_hay_configuracion():
    error_no_confi = Toplevel(root)
    error_no_confi.title("ERROR")
    error_no_confi.geometry("470x100")

    mensaje_del_error = Label(error_no_confi, text="ERROR: no se puede acceder hasta que la configuración se haya realizado.").place(x=20, y=10)

    button = Button(error_no_confi, text="Volver", command=error_no_confi.destroy).place(x=205, y=50)

#================= VALIDACIÓN DE CONFIGURACIONES ===================
#Las funciones del siguiente apartado tienen como función validar los datos de la configuración.
#Salidas: permite el llamado a la función aceptar configuraciones

#Entrada: Cantidad de espacios en el parqueo
def validate_espacios(input):
    if input == "":
        return True
    try:
        number = int(input)
        if 1 <= number:
            return True
        else:
            messagebox.showerror("Error", "Error: La cantidad mínima de espacios es 1.")
            return False
    except:
        messagebox.showerror("Error", "Error: El valor ingresado no es un número entero.")
        return False

#Entrada: Precio del parqueo por hora
def validate_precio_hora(input):
    if input == "":
        return True
    try:
        number = float(input)
        if number < 0:
            messagebox.showerror("Error", "Error: El precio por hora debe ser igual o mayor a 0.")
            return False
        if len(input.split(".")[1]) > 2:
            messagebox.showerror("Error", "Error: El precio por hora debe tener como máximo 2 decimales.")
            return False
        return True
    except ValueError:
        messagebox.showerror("Error", "Error: El valor ingresado no es un número.")
        return False
    except IndexError:
        return True

#Entrada: Pago mímino por usar el parqueo
def validate_pago_minimo(input):
    if input == "":
        return True
    try:
        number = int(input)
        if 0 <= number:
            return True
        else:
            messagebox.showerror("Error", "Error: El pago minimo es 0.")
            return False
    except:
        messagebox.showerror("Error", "Error: El valor ingresado no es un número entero.")
        return False

#Entrada: Tiempo a redondear al proximo minuto
def validate_redondear_minuto(input):
    if input == "":
        return True
    try:
        number = int(input)
        if 0 <= number <= 60:
            return True
        else:
            messagebox.showerror("Error", "Error: El minuto mínimo puede ser entre 0 y 60.")
            return False
    except:
        messagebox.showerror("Error", "Error: El valor ingresado no es un número entero.")
        return False

#Entrada: Tiempo para salir después de haber pagado
def validate_salir_pago(input):
    if input == "":
        return True
    try:
        number = int(input)
        if 0 <= number:
            return True
        else:
            messagebox.showerror("Error", "Error: El minimo de minutos para máximos para salir es 0.")
            return False
    except:
        messagebox.showerror("Error", "Error: El valor ingresado no es un número entero.")
        return False

#Entrada: lista de monedas
def verificar_monedas(monedas):
    for i in range(len(monedas)-1):
        if monedas[i] == 0 and monedas[i+1] != 0:
            messagebox.showerror("Error", "Cada moneda debe ser mayor a la anterior y si una moneda es 0, las denominaciones superiores también.")
            abrir_configuracion()
        if monedas[i] != 0 and monedas[i+1] == 0:
            messagebox.showerror("Error", "Cada moneda debe ser mayor a la anterior y si una moneda es 0, las denominaciones superiores también.")
            abrir_configuracion()
        if monedas[i] != 0 and monedas[i+1] != 0 and monedas[i+1] <= monedas[i]:
            messagebox.showerror("Error", "Cada moneda debe ser mayor a la anterior y si una moneda es 0, las denominaciones superiores también.")
            abrir_configuracion()
    return True

#Entrada: lista de billetes
def verificar_billetes(billetes):
    for i in range(len(billetes)-1):
        if billetes[i] == 0 and billetes[i+1] != 0:
            messagebox.showerror("Error", "Cada billete debe ser mayor al anterior y si un billete es 0, las denominaciones superiores también deben serlo.")
            abrir_configuracion()
        if billetes[i] != 0 and billetes[i+1] == 0:
            messagebox.showerror("Error", "Cada billete debe ser mayor al anterior y si un billete es 0, las denominaciones superiores también deben serlo.")
            abrir_configuracion()
        if billetes[i] != 0 and billetes[i+1] != 0 and billetes[i+1] <= billetes[i]:
            messagebox.showerror("Error", "Cada billete debe ser mayor al anterior y si un billete es 0, las denominaciones superiores también deben serlo.")
            abrir_configuracion()
    return True

def validate_cargar(input):
    if input == "":
        return True
    try:
        number = int(input)
        if 0 <= number:
            return True
        else:
            messagebox.showerror("Error", "El número debe ser mayor o igual a 1.")
            return False
    except:
        messagebox.showerror("Error", "El valor ingresado no es un número entero.")
        return False
#=================================================================

#Función: vaciar el dinero del cajero
#Entradas: tipos_monedas, tipos_billetes, cantidades_monedas, cantidades_billetes, salidas_monedas, salidas_billetes
#Salidas: deja en 0 los valores que están en los diccionarios de las entradas.
def vaciar_cajero():
    if vaciar.get() == 1:
        global diccionario_configuracion
        global tipos_monedas
        global cantidades_monedas
        global tipos_billetes
        global cantidades_billetes
        global salidas_monedas
        global salidas_billetes

        diccionario_configuracion["moneda1"] = 0
        diccionario_configuracion["moneda2"] = 0
        diccionario_configuracion["moneda3"] = 0
        diccionario_configuracion["billete1"] = 0
        diccionario_configuracion["billete2"] = 0
        diccionario_configuracion["billete3"] = 0
        diccionario_configuracion["billete4"] = 0
        diccionario_configuracion["billete5"] = 0

        tipos_monedas = {'moneda1': 0, 'moneda2': 0, 'moneda3': 0}
        cantidades_monedas = {'moneda1': 0, 'moneda2': 0, 'moneda3': 0}

        tipos_billetes = {'billete1': 0, 'billete2': 0, 'billete3': 0, 'billete4': 0, 'billete5': 0}
        cantidades_billetes = {'billete1': 0, 'billete2': 0, 'billete3': 0, 'billete4': 0, 'billete5': 0}

        salidas_monedas = {'moneda1': 0, 'moneda2': 0, 'moneda3': 0}
        salidas_billetes = {'billete1': 0, 'billete2': 0, 'billete3': 0, 'billete4': 0, 'billete5': 0}
        vaciar.set(0)
        mostrar_pagina_inicio()
    
    else:
        error_opcion = Toplevel(root)
        error_opcion.title("ERROR")
        error_opcion.geometry("300x100")
        mensaje_opcion = Label(error_opcion, text="ERROR: la opción vaciar cajero no fue seleccionada.").place(x=20, y=10)
        
        button = Button(error_opcion, text="Volver", command=error_opcion.destroy).place(x=130, y=50)

#Función: Validación de la placa
def validate_placa(input):
    if input == "":
        return True
    try:
        placa = str(input)
        if 1 <= len(placa) <= 8:
            return True
        else:
            messagebox.showerror("Error", "La placa puede tener de 1 a 8 caracteres.")
            return False
    except:
        messagebox.showerror("Error", "La placa puede tener de 1 a 8 caracteres.")
        return False

#Función: placa ya encontrada
#Entradas: revisa el entry para ingresar un vehículo al parqueo
#Salidas: despliega la ventana de error indicando que el vehículo ya está dentro del estacionamiento.
def error_placa_encontrada():
    error_placa = Toplevel(root)
    error_placa.title("ERROR")
    error_placa.geometry("750x100")
    
    mensaje_placa = Label(error_placa, text="ERROR: este vehículo ya se encuentra dentro del estacionamiento, por lo tanto no se puede volver a registrar hasta que el mismo salga.").place(x=20, y=10)
    
    button = Button(error_placa, text="Volver", command=error_placa.destroy).place(x=335, y=50)

#Función: ajustar tiempo
#Entradas: minutos, horas, tiempo a redondear
#salidas: redondeo
def ajustar_tiempo(horas, minutos, redondear_hasta):
    # Asegurarse de que redondear_hasta esté en el rango válido de 0 a 59
    if redondear_hasta < 0 or redondear_hasta >= 60:
        raise ValueError("El valor de redondear_hasta debe estar entre 0 y 59 inclusive.")

    # Sumamos minutos hasta que los minutos actuales sean iguales a redondear_hasta
    while minutos != redondear_hasta:
        minutos += 1
        if minutos == 60:
            minutos = 0
            horas += 1

    return horas, minutos

#Función: valida tarjeta
#Entradas: tarjeta
#salidas: True si es válida, sino despliega mensaje de error
def validate_tarjeta(input):
    if input == "":
        return True
    try:
        number = int(input)
        if 0 <= number <= 9999999999:
            return True
        else:
            messagebox.showerror("Error", "El número debe estar entre 1 y 99999999.")
            return False
    except:
        messagebox.showerror("Error", "El valor ingresado no es un número entero.")
        return False

#Función: sobrepaso de tiempo
#Entradas: minutos
#salidas: indica que el tiempo se ha sobrepasado para salir
def tiempo_sobrepasado(minutos):
    error_tiempo = Toplevel(root)
    error_tiempo.title("ERROR")
    error_tiempo.geometry("580x180")
    
    mensaje_lleno = Label(error_tiempo, text="ERROR: No puede salir porque excedió el tiempo permitido para ello.", font=("Arial", 12, "bold"), fg="red").place(x=20, y=10)
    maximo = Label(error_tiempo, text=f"Tiempo máximo para salir luego de pagar {diccionario_configuracion["minutos_maximos_salir"]} min.", font=("Arial", 12, "bold"), fg="red").place(x=20, y=40)
    pasados = Label(error_tiempo, text=f"Tiempo que usted ha tardado {int(minutos)} min.", font=("Arial", 12, "bold"), fg="red").place(x=20, y=70)
    regresar = Label(error_tiempo, text="Debe regresar al cajero a pagar la diferencia.", font=("Arial", 12, "bold"), fg="red").place(x=20, y=100)
    
    button = Button(error_tiempo, text="Volver", command=error_tiempo.destroy).place(x=205, y=130)

#Función: verificar parqueo vacio
#Entradas: parqueo
#salidas: verifica si el parqueo esta vacio
def verificar_parqueo_vacio(parqueo):
        for espacio in parqueo:
            if espacio:
                return False
        return True

#Función: error vacio
#Entradas: n/a
#salidas: indica que el parqueo esta vacio
def error_parqueo_vacio():
    error_p_vacio = Toplevel(root)
    error_p_vacio.title("ERROR")
    error_p_vacio.geometry("540x100")
    
    mensaje_lleno = Label(error_p_vacio, text="ERROR: En el parqueo no se encuentran vehículos, no se puede acceder a esta funcionalidad.").place(x=20, y=10)
    
    button = Button(error_p_vacio, text="Volver", command=error_p_vacio.destroy).place(x=255, y=50)
#________________________________________________________________________________________________________________________________________
#_____________________________________________________________CONFIGURACIÓN______________________________________________________________
#Función: Configuración
#Entradas: diferentes entrys que establecerán la configuración del estacionamiento, botones para aceptar o cancelar
#Salidas: Si se usa el boton de aceptar, se hace un llamado a la función guardar configuración, de lo contrario se vuelve al menú principal
def abrir_configuracion():
    if parqueo != []:
        for espacio in parqueo:
            if espacio != []:
                error_modificar_configuracion()
                return
    limpiar_ventana()

    def verificar_entrada():
        espacios = cantidad_espacios.get()
        if not espacios:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        precio = precio_por_hora.get()
        if not precio:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        minimo = pago_minimo.get()
        if not minimo:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        maxi = minutos_maximos_salir.get()
        if not maxi:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        mon1 = moneda1.get()
        if not mon1:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        mon2 = moneda2.get()
        if not mon2:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        mon3 = moneda3.get()
        if not mon3:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        bill1 = billete1.get()
        if not bill1:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        bill2 = billete1.get()
        if not bill2:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        bill3 = billete3.get()
        if not bill3:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        bill4 = billete4.get()
        if not bill4:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        bill5 = billete5.get()
        if not bill5:
            messagebox.showerror("Error", "Cada dato debe ser llenado.")
            return
        aceptar_configuraciones()

    titulo_saldo_cafero = Label(root, text="ESTACIONAMIENTO - CONFIGURACIÓN", font=("Times New Roman", 14)).place(x=5, y=10)
    
    vali_confi = (root.register(validate_espacios), '%P')
    mensaje_espacios = Label(root, text="Cantidad de espacios en el parqueo:").place(x=10, y=50)
    espacios_entry = Entry(root, width=20, textvariable=cantidad_espacios, validate="key", validatecommand=vali_confi).place(x=500, y=50)

    vali_precio = (root.register(validate_precio_hora), '%P')
    mensaje_precio = Label(root, text="Precio por hora:").place(x=10, y=90)
    precio_entry = Entry(root, width=20, textvariable=precio_por_hora, validate="key", validatecommand=vali_precio).place(x=500, y=90)

    vali_min = (root.register(validate_pago_minimo), '%P')
    mensaje_pago = Label(root, text="Pago mínimo:").place(x=10, y=130)
    pago_entry = Entry(root, width=20, textvariable=pago_minimo, validate="key", validatecommand=vali_min).place(x=500, y=130)

    vali_minuto = (root.register(validate_redondear_minuto), '%P')
    mensaje_redondear = Label(root, text="Redondear el tiempo cobrado al próximo minuto:").place(x=10, y=170)
    redondear_entry = Entry(root, width=20, textvariable=redondear_minuto, validate="key", validatecommand=vali_minuto).place(x=500, y=170)

    vali_salir = (root.register(validate_salir_pago), '%P')
    mensaje_minutos_salida = Label(root, text="Minutos máximos para salir después del pago:").place(x=10, y=210)
    minutos_salida_entry = Entry(root, width=20, textvariable=minutos_maximos_salir, validate="key", validatecommand=vali_salir).place(x=500, y=210)

    tipos_monedas = Label(root, text="Tipos de monedas:").place(x=10, y=250)

    mensaje_m1 = Label(root, text="Moneda 1:").place(x=10, y=290)
    moneda_m1 = Entry(root, width=20, textvariable=moneda1).place(x=500, y=290)

    mensaje_m2 = Label(root, text="Moneda 2:").place(x=10, y=330)
    moneda_m2 = Entry(root, width=20, textvariable=moneda2).place(x=500, y=330)

    mensaje_m3 = Label(root, text="Moneda 3:").place(x=10, y=370)
    moneda_me3 = Entry(root, width=20, textvariable=moneda3).place(x=500, y=370)

    tipos_billetes = Label(root, text="Tipos de billetes:").place(x=10, y=410)

    mensaje_b1 = Label(root, text="Billete 1:").place(x=10, y=450)
    billete_1 = Entry(root, width=20, textvariable=billete1).place(x=500, y=450)

    mensaje_b2 = Label(root, text="Billete 2:").place(x=10, y=490)
    billete_2 = Entry(root, width=20, textvariable=billete2).place(x=500, y=490)

    mensaje_b3 = Label(root, text="Billete 3:").place(x=10, y=530)
    billete_3 = Entry(root, width=20, textvariable=billete3).place(x=500, y=530)

    mensaje_b4 = Label(root, text="Billete 4:").place(x=10, y=570)
    billete_4 = Entry(root, width=20, textvariable=billete4).place(x=500, y=570)

    mensaje_b5 = Label(root, text="Billete 5:").place(x=10, y=610)
    billete_5 = Entry(root, width=20, textvariable=billete5).place(x=500, y=610)

    #Botones para aceptar cambios
    Button(root, text="Aceptar", command=verificar_entrada).place(x=100, y=650)
    Button(root, text="Cancelar", command=mostrar_pagina_inicio).place(x=200, y=650)

#___________________________________________________________DINERO DEL CAJERO____________________________________________________________
#Función: ver y vaciar saldo del cajero
#Entradas: una caja que se puede marcar y 2 botones
#Salidas: posiblidadad de vaciar la caja o volver al menú principal
def abrir_saldo_cajero():
    if existe_configuracion == False:
        error_no_hay_configuracion()
        return
    limpiar_ventana()
    titulo_saldo_cafero = Label(root, text="ESTACIONAMIENTO - SALDO DEL CAJERO", font=("Times New Roman", 14)).place(x=5, y=10)

    denominacion = Label(root, text="DENOMINACIÓN").place(x=0, y=55)
    monedas_deno1 = Label(root, text=f"Monedas de {tipos_monedas["moneda1"]}").place(x=0, y=80)
    monedas_deno2 = Label(root, text=f"Monedas de {tipos_monedas["moneda2"]}").place(x=0, y=100)
    monedas_deno3 = Label(root, text=f"Monedas de {tipos_monedas["moneda3"]}").place(x=0, y=120)
    total_monedas_deno = Label(root, text="TOTAL DE MONEDAS").place(x=0, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_deno1 = Label(root, text=f"Billetes de {tipos_billetes["billete1"]}").place(x=0, y=180)
    billetes_deno2 = Label(root, text=f"Billetes de {tipos_billetes["billete2"]}").place(x=0, y=200)
    billetes_deno3 = Label(root, text=f"Billetes de {tipos_billetes["billete3"]}").place(x=0, y=220)
    billetes_deno4 = Label(root, text=f"Billetes de {tipos_billetes["billete4"]}").place(x=0, y=240)
    billetes_deno5 = Label(root, text=f"Billetes de {tipos_billetes["billete5"]}").place(x=0, y=260)
    total_billetes_deno = Label(root, text="TOTAL DE BILLETES").place(x=0, y=285)

    saldo_antes_carga = Label(root, text="ENTRADAS").place(x=220, y=35)
    cantidad_antes = Label(root, text="CANTIDAD").place(x=180, y=55)
    monedas_cantidad1 = Label(root, text=f"{cantidades_monedas["moneda1"]}").place(x=180, y=80)
    monedas_cantidad2 = Label(root, text=f"{cantidades_monedas["moneda2"]}").place(x=180, y=100)
    monedas_cantidad3 = Label(root, text=f"{cantidades_monedas["moneda3"]}").place(x=180, y=120)
    cantidad_monedas = Label(root, text=f"{cantidades_monedas["moneda1"] + cantidades_monedas["moneda2"] + cantidades_monedas["moneda3"]}").place(x=180, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_cantidad1 = Label(root, text=f"{cantidades_billetes["billete1"]}").place(x=180, y=180)
    billetes_cantidad2 = Label(root, text=f"{cantidades_billetes["billete2"]}").place(x=180, y=200)
    billetes_cantidad3 = Label(root, text=f"{cantidades_billetes["billete3"]}").place(x=180, y=220)
    billetes_cantidad4 = Label(root, text=f"{cantidades_billetes["billete4"]}").place(x=180, y=240)
    billetes_cantidad5 = Label(root, text=f"{cantidades_billetes["billete5"]}").place(x=180, y=260)
    cantidad_billetes  = Label(root, text=f"{cantidades_billetes["billete1"] + cantidades_billetes["billete2"] + cantidades_billetes["billete3"] + cantidades_billetes["billete4"] + cantidades_billetes["billete5"]}").place(x=180, y=285)
    #====================================================================================================
    total_antes = Label(root, text="TOTAL").place(x=270, y=55)
    monedas_total1 = Label(root, text=f"{tipos_monedas["moneda1"] * cantidades_monedas["moneda1"]}").place(x=270, y=80)
    monedas_total2 = Label(root, text=f"{tipos_monedas["moneda2"] * cantidades_monedas["moneda2"]}").place(x=270, y=100)
    monedas_total3 = Label(root, text=f"{tipos_monedas["moneda3"] * cantidades_monedas["moneda3"]}").place(x=270, y=120)
    total_monedas_total = Label(root, text=f"{tipos_monedas["moneda1"] * cantidades_monedas["moneda1"] + tipos_monedas["moneda2"] * cantidades_monedas["moneda2"] + tipos_monedas["moneda3"] * cantidades_monedas["moneda3"]}").place(x=270, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_total1 = Label(root, text=f"{tipos_billetes["billete1"] * cantidades_billetes["billete1"]}").place(x=270, y=180)
    billetes_total2 = Label(root, text=f"{tipos_billetes["billete2"] * cantidades_billetes["billete2"]}").place(x=270, y=200)
    billetes_total3 = Label(root, text=f"{tipos_billetes["billete3"] * cantidades_billetes["billete3"]}").place(x=270, y=220)
    billetes_total4 = Label(root, text=f"{tipos_billetes["billete4"] * cantidades_billetes["billete4"]}").place(x=270, y=240)
    billetes_total5 = Label(root, text=f"{tipos_billetes["billete5"] * cantidades_billetes["billete5"]}").place(x=270, y=260)
    total_billetes_total = Label(root, text=f"{tipos_billetes["billete1"] * cantidades_billetes["billete1"] + tipos_billetes["billete2"] * cantidades_billetes["billete2"] + tipos_billetes["billete3"] * cantidades_billetes["billete3"] + tipos_billetes["billete4"] * cantidades_billetes["billete4"] + tipos_billetes["billete5"] * cantidades_billetes["billete5"]}").place(x=270, y=285)
    
    salidas = Label(root, text="SALIDAS").place(x=460, y=35)
    cantidad_salida = Label(root, text="CANTIDAD").place(x=400, y=55)
    monedas_salida1 = Label(root, text=f"{salidas_monedas["moneda1"]}").place(x=400, y=80)
    monedas_salida2 = Label(root, text=f"{salidas_monedas["moneda2"]}").place(x=400, y=100)
    monedas_salida3 = Label(root, text=f"{salidas_monedas["moneda3"]}").place(x=400, y=120)
    total_cantidad_salida_monedas = Label(root, text=f"{salidas_monedas["moneda1"] + salidas_monedas["moneda2"] + salidas_monedas["moneda3"]}").place(x=400, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_salida1 = Label(root, text=f"{salidas_billetes["billete1"]}").place(x=400, y=180)
    billetes_salida2 = Label(root, text=f"{salidas_billetes["billete2"]}").place(x=400, y=200)
    billetes_salida3 = Label(root, text=f"{salidas_billetes["billete3"]}").place(x=400, y=220)
    billetes_salida4 = Label(root, text=f"{salidas_billetes["billete4"]}").place(x=400, y=240)
    billetes_salida5 = Label(root, text=f"{salidas_billetes["billete5"]}").place(x=400, y=260)
    cantidad_billetes_salida  = Label(root, text=f"{salidas_billetes["billete1"] + salidas_billetes["billete2"] + salidas_billetes["billete3"] + salidas_billetes["billete4"] + salidas_billetes["billete5"]}").place(x=400, y=285)
    #====================================================================================================
    total_salida = Label(root, text="TOTAL").place(x=500, y=55)
    monedas_salida_total1 = Label(root, text=f"{tipos_monedas["moneda1"] * salidas_monedas["moneda1"]}").place(x=500, y=80)
    monedas_salida_total2 = Label(root, text=f"{tipos_monedas["moneda2"] * salidas_monedas["moneda2"]}").place(x=500, y=100)
    monedas_salida_total3 = Label(root, text=f"{tipos_monedas["moneda3"] * salidas_monedas["moneda3"]}").place(x=500, y=120)
    total_monedas_salida = Label(root, text=f"{tipos_monedas["moneda1"] * salidas_monedas["moneda1"] + tipos_monedas["moneda2"] * salidas_monedas["moneda2"] + tipos_monedas["moneda3"] * salidas_monedas["moneda3"]}").place(x=500, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_salida_total1 = Label(root, text=f"{tipos_billetes["billete1"] * salidas_billetes["billete1"]}").place(x=500, y=180)
    billetes_salida_total2 = Label(root, text=f"{tipos_billetes["billete2"] * salidas_billetes["billete2"]}").place(x=500, y=200)
    billetes_salida_total3 = Label(root, text=f"{tipos_billetes["billete3"] * salidas_billetes["billete3"]}").place(x=500, y=220)
    billetes_salida_total4 = Label(root, text=f"{tipos_billetes["billete4"] * salidas_billetes["billete4"]}").place(x=500, y=240)
    billetes_salida_total5 = Label(root, text=f"{tipos_billetes["billete5"] * salidas_billetes["billete5"]}").place(x=500, y=260)
    total_billetes_salida = Label(root, text=f"{tipos_billetes["billete1"] * salidas_billetes["billete1"] + tipos_billetes["billete2"] * salidas_billetes["billete2"] + tipos_billetes["billete3"] * salidas_billetes["billete3"] + tipos_billetes["billete4"] * salidas_billetes["billete4"] + tipos_billetes["billete5"] * salidas_billetes["billete5"]}").place(x=500, y=285)

    saldo = Label(root, text="SALDO").place(x=675, y=35)
    cantidad_saldo = Label(root, text="CANTIDAD").place(x=615, y=55)
    monedas_salida1 = Label(root, text=f"{cantidades_monedas["moneda1"] - salidas_monedas["moneda1"]}").place(x=615, y=80)
    monedas_salida2 = Label(root, text=f"{cantidades_monedas["moneda2"] - salidas_monedas["moneda2"]}").place(x=615, y=100)
    monedas_salida3 = Label(root, text=f"{cantidades_monedas["moneda3"] - salidas_monedas["moneda3"]}").place(x=615, y=120)
    total_cantidad_salida_monedas = Label(root, text=f"{(cantidades_monedas["moneda1"] - salidas_monedas["moneda1"]) + (cantidades_monedas["moneda2"] - salidas_monedas["moneda2"]) + (cantidades_monedas["moneda3"] - salidas_monedas["moneda3"])}").place(x=615, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_salida1 = Label(root, text=f"{cantidades_billetes["billete1"] - salidas_billetes["billete1"]}").place(x=615, y=180)
    billetes_salida2 = Label(root, text=f"{cantidades_billetes["billete2"] -  salidas_billetes["billete2"]}").place(x=615, y=200)
    billetes_salida3 = Label(root, text=f"{cantidades_billetes["billete3"] - salidas_billetes["billete3"]}").place(x=615, y=220)
    billetes_salida4 = Label(root, text=f"{cantidades_billetes["billete4"] - salidas_billetes["billete4"]}").place(x=615, y=240)
    billetes_salida5 = Label(root, text=f"{cantidades_billetes["billete5"] - salidas_billetes["billete5"]}").place(x=615, y=260)
    cantidad_billetes_salida  = Label(root, text= f"{(cantidades_billetes["billete1"] - salidas_billetes["billete1"]) + (cantidades_billetes["billete2"] -  salidas_billetes["billete2"]) + (cantidades_billetes["billete3"] - salidas_billetes["billete3"]) + (cantidades_billetes["billete4"] - salidas_billetes["billete4"]) + (cantidades_billetes["billete5"] - salidas_billetes["billete5"])}").place(x=615, y=285)
    #====================================================================================================
    total_saldo = Label(root, text="TOTAL").place(x=715, y=55)
    monedas_salida_total1 = Label(root, text=f"{(tipos_monedas["moneda1"] * cantidades_monedas["moneda1"]) - (tipos_monedas["moneda1"] * salidas_monedas["moneda1"])}").place(x=715, y=80)
    monedas_salida_total2 = Label(root, text=f"{(tipos_monedas["moneda2"] * cantidades_monedas["moneda2"]) - (tipos_monedas["moneda2"] * salidas_monedas["moneda2"])}").place(x=715, y=100)
    monedas_salida_total3 = Label(root, text=f"{(tipos_monedas["moneda3"] * cantidades_monedas["moneda3"]) - (tipos_monedas["moneda3"] * salidas_monedas["moneda3"])}").place(x=715, y=120)
    total_monedas_salida = Label(root, text=f"{(tipos_monedas["moneda1"] * cantidades_monedas["moneda1"]) - (tipos_monedas["moneda1"] * salidas_monedas["moneda1"]) + (tipos_monedas["moneda2"] * cantidades_monedas["moneda2"]) - (tipos_monedas["moneda2"] * salidas_monedas["moneda2"]) + (tipos_monedas["moneda3"] * cantidades_monedas["moneda3"]) - (tipos_monedas["moneda3"] * salidas_monedas["moneda3"])}").place(x=715, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_salida_total1 = Label(root, text=f"{(tipos_billetes["billete1"] * cantidades_billetes["billete1"]) - (tipos_billetes["billete1"] * salidas_billetes["billete1"])}").place(x=715, y=180)
    billetes_salida_total2 = Label(root, text=f"{(tipos_billetes["billete2"] * cantidades_billetes["billete2"]) - (tipos_billetes["billete2"] * salidas_billetes["billete2"])}").place(x=715, y=200)
    billetes_salida_total3 = Label(root, text=f"{(tipos_billetes["billete3"] * cantidades_billetes["billete3"]) - (tipos_billetes["billete3"] * salidas_billetes["billete3"])}").place(x=715, y=220)
    billetes_salida_total4 = Label(root, text=f"{(tipos_billetes["billete4"] * cantidades_billetes["billete4"]) - (tipos_billetes["billete4"] * salidas_billetes["billete4"])}").place(x=715, y=240)
    billetes_salida_total5 = Label(root, text=f"{(tipos_billetes["billete5"] * cantidades_billetes["billete5"]) - (tipos_billetes["billete5"] * salidas_billetes["billete5"])}").place(x=715, y=260)
    total_billetes_salida = Label(root, text=f"{((tipos_billetes["billete1"] * cantidades_billetes["billete1"]) - (tipos_billetes["billete1"] * salidas_billetes["billete1"])) + ((tipos_billetes["billete2"] * cantidades_billetes["billete2"]) - (tipos_billetes["billete2"] * salidas_billetes["billete2"])) + ((tipos_billetes["billete3"] * cantidades_billetes["billete3"]) - (tipos_billetes["billete3"] * salidas_billetes["billete3"])) + ((tipos_billetes["billete4"] * cantidades_billetes["billete4"]) - (tipos_billetes["billete4"] * salidas_billetes["billete4"])) + ((tipos_billetes["billete5"] * cantidades_billetes["billete5"]) - (tipos_billetes["billete5"] * salidas_billetes["billete5"]))}").place(x=715, y=285)


    opcion = Checkbutton(root, text="Vaciar cajero", variable=vaciar).place(x=10, y=315)

    Button(root, text="Aceptar", command=vaciar_cajero).place(x=100, y=350)
    Button(root, text="Cancelar", command=mostrar_pagina_inicio).place(x=200, y=350)

#Función: cargar cajero
#Entradas: cantidades de denominaciones para cargar al cajero
#Salidas: Adición de montos al cajero
def abrir_cargar_cajero():
    if existe_configuracion == False:
        error_no_hay_configuracion()
        return
    limpiar_ventana()

    titulo_saldo_cafero = Label(root, text="ESTACIONAMIENTO - SALDO DEL CAJERO", font=("Times New Roman", 14)).place(x=5, y=10)

    denominacion = Label(root, text="DENOMINACIÓN").place(x=0, y=55)
    monedas_deno1 = Label(root, text=f"Monedas de {tipos_monedas["moneda1"]}").place(x=0, y=80)
    monedas_deno2 = Label(root, text=f"Monedas de {tipos_monedas["moneda2"]}").place(x=0, y=100)
    monedas_deno3 = Label(root, text=f"Monedas de {tipos_monedas["moneda3"]}").place(x=0, y=120)
    total_monedas_deno = Label(root, text="TOTAL DE MONEDAS").place(x=0, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_deno1 = Label(root, text=f"Billetes de {tipos_billetes["billete1"]}").place(x=0, y=180)
    billetes_deno2 = Label(root, text=f"Billetes de {tipos_billetes["billete2"]}").place(x=0, y=200)
    billetes_deno3 = Label(root, text=f"Billetes de {tipos_billetes["billete3"]}").place(x=0, y=220)
    billetes_deno4 = Label(root, text=f"Billetes de {tipos_billetes["billete4"]}").place(x=0, y=240)
    billetes_deno5 = Label(root, text=f"Billetes de {tipos_billetes["billete5"]}").place(x=0, y=260)
    total_billetes_deno = Label(root, text="TOTAL DE BILLETES").place(x=0, y=285)

    saldo_antes_carga = Label(root, text="SALDO ANTES DE LA CARGA").place(x=167, y=35)
    cantidad_antes = Label(root, text="CANTIDAD").place(x=180, y=55)
    monedas_cantidad1 = Label(root, text=f"{cantidades_monedas["moneda1"]}").place(x=180, y=80)
    monedas_cantidad2 = Label(root, text=f"{cantidades_monedas["moneda2"]}").place(x=180, y=100)
    monedas_cantidad3 = Label(root, text=f"{cantidades_monedas["moneda3"]}").place(x=180, y=120)
    cantidad_monedas = Label(root, text=f"{cantidades_monedas["moneda1"] + cantidades_monedas["moneda2"] + cantidades_monedas["moneda3"]}").place(x=180, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_cantidad1 = Label(root, text=f"{cantidades_billetes["billete1"]}").place(x=180, y=180)
    billetes_cantidad2 = Label(root, text=f"{cantidades_billetes["billete2"]}").place(x=180, y=200)
    billetes_cantidad3 = Label(root, text=f"{cantidades_billetes["billete3"]}").place(x=180, y=220)
    billetes_cantidad4 = Label(root, text=f"{cantidades_billetes["billete4"]}").place(x=180, y=240)
    billetes_cantidad5 = Label(root, text=f"{cantidades_billetes["billete5"]}").place(x=180, y=260)
    cantidad_billetes  = Label(root, text=f"{cantidades_billetes["billete1"] + cantidades_billetes["billete2"] + cantidades_billetes["billete3"] + cantidades_billetes["billete4"] + cantidades_billetes["billete5"]}").place(x=180, y=285)
    #====================================================================================================
    total_antes = Label(root, text="TOTAL").place(x=270, y=55)
    monedas_total1 = Label(root, text=f"{tipos_monedas["moneda1"] * cantidades_monedas["moneda1"]}").place(x=270, y=80)
    monedas_total2 = Label(root, text=f"{tipos_monedas["moneda2"] * cantidades_monedas["moneda2"]}").place(x=270, y=100)
    monedas_total3 = Label(root, text=f"{tipos_monedas["moneda3"] * cantidades_monedas["moneda3"]}").place(x=270, y=120)
    total_monedas_total = Label(root, text=f"{tipos_monedas["moneda1"] * cantidades_monedas["moneda1"] + tipos_monedas["moneda2"] * cantidades_monedas["moneda2"] + tipos_monedas["moneda3"] * cantidades_monedas["moneda3"]}").place(x=270, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_total1 = Label(root, text=f"{tipos_billetes["billete1"] * cantidades_billetes["billete1"]}").place(x=270, y=180)
    billetes_total2 = Label(root, text=f"{tipos_billetes["billete2"] * cantidades_billetes["billete2"]}").place(x=270, y=200)
    billetes_total3 = Label(root, text=f"{tipos_billetes["billete3"] * cantidades_billetes["billete3"]}").place(x=270, y=220)
    billetes_total4 = Label(root, text=f"{tipos_billetes["billete4"] * cantidades_billetes["billete4"]}").place(x=270, y=240)
    billetes_total5 = Label(root, text=f"{tipos_billetes["billete5"] * cantidades_billetes["billete5"]}").place(x=270, y=260)
    total_billetes_total = Label(root, text=f"{tipos_billetes["billete1"] * cantidades_billetes["billete1"] + tipos_billetes["billete2"] * cantidades_billetes["billete2"] + tipos_billetes["billete3"] * cantidades_billetes["billete3"] + tipos_billetes["billete4"] * cantidades_billetes["billete4"] + tipos_billetes["billete5"] * cantidades_billetes["billete5"]}").place(x=270, y=285)
    
    def actualizar_resultado(event):
        #Carga
        try:
            numero = int(carga_moneda1.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = numero * tipos_monedas["moneda1"]
                monedas_carga_total1.config(text=f"{resultado}")
        except:
            monedas_carga_total1.config(text=f"número inválido")
        try:
            numero = int(carga_moneda2.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = numero * tipos_monedas["moneda2"]
                monedas_carga_total2.config(text=f"{resultado}")
        except:
            monedas_carga_total2.config(text=f"número inválido")
        try:
            numero = int(carga_moneda3.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = numero * tipos_monedas["moneda3"]
                monedas_carga_total3.config(text=f"{resultado}")
        except:
            monedas_carga_total3.config(text=f"número inválido")

        try:
            numero = int(carga_billete1.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = numero * tipos_billetes["billete1"]
                billetes_carga_total1.config(text=f"{resultado}")
        except:
            billetes_carga_total1.config(text=f"número inválido")
        try:
            numero = int(carga_billete2.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = numero * tipos_billetes["billete2"] 
                billetes_carga_total2.config(text=f"{resultado}")
        except:
            billetes_carga_total2.config(text=f"número inválido")
        try:
            numero = int(carga_billete3.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = numero * tipos_billetes["billete3"]
                billetes_carga_total3.config(text=f"{resultado}")
        except:
            billetes_carga_total3.config(text=f"número inválido")
        try:
            numero = int(carga_billete4.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = numero * tipos_billetes["billete4"]
                billetes_carga_total4.config(text=f"{resultado}")
        except:
            billetes_carga_total4.config(text=f"número inválido")
        try:
            numero = int(carga_billete5.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = numero * tipos_billetes["billete5"]
                billetes_carga_total5.config(text=f"{resultado}")
        except:
            billetes_carga_total5.config(text=f"número inválido")
        #________________________________________________________________
        #Saldo
        try:
            numero = int(carga_moneda1.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = cantidades_monedas["moneda1"] + numero
                monedas_saldo1.config(text=f"{resultado}")
        except:
            monedas_saldo1.config(text=f"número inválido")
        try:
            numero = int(carga_moneda2.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = cantidades_monedas["moneda2"] + numero
                monedas_saldo2.config(text=f"{resultado}")
        except:
            monedas_saldo2.config(text=f"número inválido")
        try:
            numero = int(carga_moneda3.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = cantidades_monedas["moneda3"] + numero
                monedas_saldo3.config(text=f"{resultado}")
        except:
            monedas_saldo3.config(text=f"número inválido")
        try:
            numero = int(carga_billete1.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = cantidades_billetes["billete1"] + numero
                billetes_saldo1.config(text=f"{resultado}")
        except:
            billetes_saldo1.config(text=f"número inválido")
        try:
            numero = int(carga_billete2.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = cantidades_billetes["billete2"] + numero
                billetes_saldo2.config(text=f"{resultado}")
        except:
            billetes_saldo2.config(text=f"número inválido")
        try:
            numero = int(carga_billete3.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = cantidades_billetes["billete1"] + numero
                billetes_saldo3.config(text=f"{resultado}")
        except:
            billetes_saldo3.config(text=f"número inválido")
        try:
            numero = int(carga_billete4.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = cantidades_billetes["billete1"] + numero
                billetes_saldo4.config(text=f"{resultado}")
        except:
            billetes_saldo4.config(text=f"número inválido")
        try:
            numero = int(carga_billete5.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = cantidades_billetes["billete5"] + numero
                billetes_saldo5.config(text=f"{resultado}")
        except:
            billetes_saldo5.config(text=f"número inválido")
        try:
            numero = int(carga_billete5.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = cantidades_billetes["billete5"] + numero
                billetes_saldo5.config(text=f"{resultado}")
        except:
            billetes_saldo5.config(text=f"número inválido")
        #saldo total
        try:
            numero = int(carga_moneda1.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = tipos_monedas["moneda1"] * numero + (tipos_monedas["moneda1"] * cantidades_monedas["moneda1"])
                monedas_saldo_total1.config(text=f"{resultado}")
        except:
            monedas_saldo_total1.config(text=f"número inválido")
        try:
            numero = int(carga_moneda2.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = tipos_monedas["moneda2"] * numero + (tipos_monedas["moneda2"] * cantidades_monedas["moneda2"])
                monedas_saldo_total2.config(text=f"{resultado}")
        except:
            monedas_saldo_total2.config(text=f"número inválido")
        try:
            numero = int(carga_moneda3.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = tipos_monedas["moneda3"] * numero + (tipos_monedas["moneda3"] * cantidades_monedas["moneda3"])
                monedas_saldo_total3.config(text=f"{resultado}")
        except:
            monedas_saldo_total3.config(text=f"número inválido")

        try:
            numero = int(carga_billete1.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = tipos_billetes["billete1"] * numero + (tipos_billetes["billete1"] * cantidades_billetes["billete1"])
                billetes_saldo_total1.config(text=f"{resultado}")
        except:
            billetes_saldo_total1.config(text=f"número inválido")
        try:
            numero = int(carga_billete2.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = tipos_billetes["billete2"] * numero + (tipos_billetes["billete2"] * cantidades_billetes["billete2"]) 
                billetes_saldo_total2.config(text=f"{resultado}")
        except:
            billetes_saldo_total2.config(text=f"número inválido")
        try:
            numero = int(carga_billete3.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = tipos_billetes["billete3"] * numero + (tipos_billetes["billete3"] * cantidades_billetes["billete3"])
                billetes_saldo_total3.config(text=f"{resultado}")
        except:
            billetes_saldo_total3.config(text=f"número inválido")
        try:
            numero = int(carga_billete4.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = tipos_billetes["billete4"] * numero + (tipos_billetes["billete4"] * cantidades_billetes["billete4"])
                billetes_saldo_total4.config(text=f"{resultado}")
        except:
            billetes_saldo_total4.config(text=f"número inválido")
        try:
            numero = int(carga_billete5.get())
            if isinstance(numero, int) == True and numero >= 0:
                resultado = tipos_billetes["billete5"] * numero + (tipos_billetes["billete5"] * cantidades_billetes["billete5"])
                billetes_saldo_total5.config(text=f"{resultado}")
        except:
            billetes_saldo_total5.config(text=f"número inválido")
        #_________________________TOTALES______________________________
        try:
            numero = int(carga_moneda1.get())
            numero2 = int(carga_moneda2.get())
            numero3 = int(carga_moneda3.get())
            
            if isinstance(numero, int) == True and numero >= 0 and isinstance(numero2, int) == True and numero2 >= 0 and isinstance(numero3, int) == True and numero3 >= 0:
                resultado = numero + numero2 + numero3
                total_cantidad_carga_monedas.config(text=f"{resultado}")
        except:
            total_cantidad_carga_monedas.config(text=f"número inválido")
        try:
            numero = int(carga_moneda1.get())
            numero2 = int(carga_moneda2.get())
            numero3 = int(carga_moneda3.get())
            
            if isinstance(numero, int) == True and numero >= 0 and isinstance(numero2, int) == True and numero2 >= 0 and isinstance(numero3, int) == True and numero3 >= 0:
                resultado = (tipos_monedas["moneda1"] * numero) + (tipos_monedas["moneda2"] * numero2) + (tipos_monedas["moneda3"] * numero3)
                total_monedas_carga.config(text=f"{resultado}")
        except:
            total_monedas_carga.config(text=f"número inválido") 
        try:
            numero = int(carga_billete1.get())
            numero2 = int(carga_billete2.get())
            numero3 = int(carga_billete3.get())
            numero4 = int(carga_billete4.get())
            numero5 = int(carga_billete5.get())
            
            if isinstance(numero, int) == True and numero >= 0 and isinstance(numero2, int) == True and numero2 >= 0 and isinstance(numero3, int) == True and numero3 >= 0 and isinstance(numero4, int) == True and numero4 >= 0 and isinstance(numero5, int) == True and numero5 >= 0:
                resultado = numero + numero2 + numero3 + numero4 + numero5
                total_cantidad_carga_billetes.config(text=f"{resultado}")
        except:
            total_cantidad_carga_billetes.config(text=f"número inválido")
        try:
            numero = int(carga_billete1.get())
            numero2 = int(carga_billete2.get())
            numero3 = int(carga_billete3.get())
            numero4 = int(carga_billete4.get())
            numero5 = int(carga_billete5.get())
            
            if isinstance(numero, int) == True and numero >= 0 and isinstance(numero2, int) == True and numero2 >= 0 and isinstance(numero3, int) == True and numero3 >= 0 and isinstance(numero4, int) == True and numero4 >= 0 and isinstance(numero5, int) == True and numero5 >= 0:
                resultado = (tipos_billetes["billete1"] * numero) + (tipos_billetes["billete2"] * numero2) + (tipos_billetes["billete3"] * numero3) + (tipos_billetes["billete4"] * numero4) + (tipos_billetes["billete5"] * numero5)
                total_billetes_carga.config(text=f"{resultado}")
        except:
            total_billetes_carga.config(text=f"número inválido")
        try:
            numero = int(carga_moneda1.get())
            numero2 = int(carga_moneda2.get())
            numero3 = int(carga_moneda3.get())
            
            if isinstance(numero, int) == True and numero >= 0 and isinstance(numero2, int) == True and numero2 >= 0 and isinstance(numero3, int) == True and numero3 >= 0:
                resultado = numero + numero2 + numero3 + cantidades_monedas["moneda1"] + cantidades_monedas["moneda2"] + cantidades_monedas["moneda3"]
                total_cantidad_saldo_monedas.config(text=f"{resultado}")
        except:
            total_cantidad_saldo_monedas.config(text=f"número inválido")
        try:
            numero = int(carga_moneda1.get())
            numero2 = int(carga_moneda2.get())
            numero3 = int(carga_moneda3.get())
            
            if isinstance(numero, int) == True and numero >= 0 and isinstance(numero2, int) == True and numero2 >= 0 and isinstance(numero3, int) == True and numero3 >= 0:
                resultado = (tipos_monedas["moneda1"] * numero) + (tipos_monedas["moneda2"] * numero2) + (tipos_monedas["moneda3"] * numero3) + (tipos_monedas["moneda1"] * cantidades_monedas["moneda1"]) + (tipos_monedas["moneda2"] * cantidades_monedas["moneda2"]) + (tipos_monedas["moneda3"] * cantidades_monedas["moneda3"])
                total_monedas_saldo.config(text=f"{resultado}")
        except:
            total_monedas_saldo.config(text=f"número inválido")
        try:
            numero = int(carga_billete1.get())
            numero2 = int(carga_billete2.get())
            numero3 = int(carga_billete3.get())
            numero4 = int(carga_billete4.get())
            numero5 = int(carga_billete5.get())
            
            if isinstance(numero, int) == True and numero >= 0 and isinstance(numero2, int) == True and numero2 >= 0 and isinstance(numero3, int) == True and numero3 >= 0 and isinstance(numero4, int) == True and numero4 >= 0 and isinstance(numero5, int) == True and numero5 >= 0:
                resultado = numero + numero2 + numero3 + numero4 + numero5 + cantidades_billetes["billete1"] + cantidades_billetes["billete2"] + cantidades_billetes["billete3"] + cantidades_billetes["billete4"] + cantidades_billetes["billete5"]
                total_cantidad_billetes_saldo.config(text=f"{resultado}")
        except:
            total_cantidad_billetes_saldo.config(text=f"número inválido")
        try:
            numero = int(carga_billete1.get())
            numero2 = int(carga_billete2.get())
            numero3 = int(carga_billete3.get())
            numero4 = int(carga_billete4.get())
            numero5 = int(carga_billete5.get())
            
            if isinstance(numero, int) == True and numero >= 0 and isinstance(numero2, int) == True and numero2 >= 0 and isinstance(numero3, int) == True and numero3 >= 0 and isinstance(numero4, int) == True and numero4 >= 0 and isinstance(numero5, int) == True and numero5 >= 0:
                resultado = (tipos_billetes["billete1"] * numero) + (tipos_billetes["billete2"] * numero2) + (tipos_billetes["billete3"] * numero3) + (tipos_billetes["billete4"] * numero4) + (tipos_billetes["billete5"] * numero5) + (tipos_billetes["billete1"] * cantidades_billetes["billete1"]) + (tipos_billetes["billete2"] * cantidades_billetes["billete2"]) + (tipos_billetes["billete3"] * cantidades_billetes["billete3"]) + (tipos_billetes["billete4"] * cantidades_billetes["billete4"]) + (tipos_billetes["billete5"] * cantidades_billetes["billete5"])
                total_billetes_saldo.config(text=f"{resultado}")
        except:
            total_billetes_saldo.config(text=f"número inválido")
        
    carga = Label(root, text="CARGA").place(x=457, y=35)
    carga_cantidad = Label(root, text="CANTIDAD").place(x=400, y=55)
    monedas_carga1 = Entry(root, width=12, textvariable=carga_moneda1)
    monedas_carga1.place(x=400, y=80)
    monedas_carga2 = Entry(root, width=12, textvariable=carga_moneda2)
    monedas_carga2.place(x=400, y=100)
    monedas_carga3 = Entry(root, width=12, textvariable=carga_moneda3)
    monedas_carga3.place(x=400, y=120)
    total_cantidad_carga_monedas = Label(root, text=f"{0}")
    total_cantidad_carga_monedas.place(x=400, y=145)

    #---------------------------------------------------------------------------------------------------
    billetes_carga1 = Entry(root, width=12, textvariable=carga_billete1)
    billetes_carga1.place(x=400, y=180)
    billetes_carga2 = Entry(root, width=12, textvariable=carga_billete2)
    billetes_carga2.place(x=400, y=200)
    billetes_carga3 = Entry(root, width=12, textvariable=carga_billete3)
    billetes_carga3.place(x=400, y=220)
    billetes_carga4 = Entry(root, width=12, textvariable=carga_billete4)
    billetes_carga4.place(x=400, y=240)
    billetes_carga5 = Entry(root, width=12, textvariable=carga_billete5)
    billetes_carga5.place(x=400, y=260)
    total_cantidad_carga_billetes = Label(root, text=f"{0}")
    total_cantidad_carga_billetes.place(x=400, y=285)

    #====================================================================================================
    total_salida = Label(root, text="TOTAL").place(x=500, y=55)
    monedas_carga_total1 = Label(root, text=f"{cantidades_monedas["moneda1"]}")
    monedas_carga_total1.place(x=500, y=80)

    monedas_carga_total2 = Label(root, text=f"{cantidades_monedas["moneda2"]}")
    monedas_carga_total2.place(x=500, y=100)

    monedas_carga_total3 = Label(root, text=f"{cantidades_monedas["moneda3"]}")
    monedas_carga_total3.place(x=500, y=120)
    total_monedas_carga = Label(root, text=f"{0}")
    total_monedas_carga.place(x=500, y=145)
    
    #---------------------------------------------------------------------------------------------------
    billetes_carga_total1 = Label(root, text=f"{0}")
    billetes_carga_total1.place(x=500, y=180)

    billetes_carga_total2 = Label(root, text=f"{0}")
    billetes_carga_total2.place(x=500, y=200)

    billetes_carga_total3 = Label(root, text=f"{0}")
    billetes_carga_total3.place(x=500, y=220)
    
    billetes_carga_total4 = Label(root, text=f"{0}")
    billetes_carga_total4.place(x=500, y=240)
    
    billetes_carga_total5 = Label(root, text=f"{0}")
    billetes_carga_total5.place(x=500, y=260)
    
    total_billetes_carga = Label(root, text=f"{0}")
    total_billetes_carga.place(x=500, y=285)

    #_______________________________________________________________________________
    saldo = Label(root, text="SALDO").place(x=675, y=35)
    cantidad_saldo = Label(root, text="CANTIDAD").place(x=615, y=55)
    monedas_saldo1 = Label(root, text=f"{cantidades_monedas["moneda1"]}")
    monedas_saldo1.place(x=615, y=80)
    
    monedas_saldo2 = Label(root, text=f"{cantidades_monedas["moneda2"]}")
    monedas_saldo2.place(x=615, y=100)
    

    monedas_saldo3 = Label(root, text=f"{cantidades_monedas["moneda3"]}")
    monedas_saldo3.place(x=615, y=120)
    
    total_cantidad_saldo_monedas = Label(root, text=f"{(cantidades_monedas["moneda1"]) + (cantidades_monedas["moneda2"]) + (cantidades_monedas["moneda3"])}")
    total_cantidad_saldo_monedas.place(x=615, y=145)
    
    #---------------------------------------------------------------------------------------------------
    billetes_saldo1 = Label(root, text=f"{cantidades_billetes["billete1"]}")
    billetes_saldo1.place(x=615, y=180)
    
    billetes_saldo2 = Label(root, text=f"{cantidades_billetes["billete2"]}")
    billetes_saldo2.place(x=615, y=200)
    
    billetes_saldo3 = Label(root, text=f"{cantidades_billetes["billete3"]}")
    billetes_saldo3.place(x=615, y=220)
    
    billetes_saldo4 = Label(root, text=f"{cantidades_billetes["billete4"]}")
    billetes_saldo4.place(x=615, y=240)
    
    billetes_saldo5 = Label(root, text=f"{cantidades_billetes["billete5"]}")
    billetes_saldo5.place(x=615, y=260)
    
    total_cantidad_billetes_saldo  = Label(root, text= f"{cantidades_billetes["billete1"] + cantidades_billetes["billete2"] + cantidades_billetes["billete3"] + cantidades_billetes["billete4"] + cantidades_billetes["billete5"]}")
    total_cantidad_billetes_saldo.place(x=615, y=285)
    
    #====================================================================================================
    total_saldo = Label(root, text="TOTAL").place(x=715, y=55)
    monedas_saldo_total1 = Label(root, text=f"{tipos_monedas["moneda1"] * cantidades_monedas["moneda1"] }")
    monedas_saldo_total1.place(x=715, y=80)
    
    monedas_saldo_total2 = Label(root, text=f"{tipos_monedas["moneda2"] * cantidades_monedas["moneda2"]}")
    monedas_saldo_total2.place(x=715, y=100)
    
    monedas_saldo_total3 = Label(root, text=f"{tipos_monedas["moneda3"] * cantidades_monedas["moneda3"]}")
    monedas_saldo_total3.place(x=715, y=120)
    
    total_monedas_saldo = Label(root, text=f"{(tipos_monedas["moneda1"] * cantidades_monedas["moneda1"]) + (tipos_monedas["moneda2"] * cantidades_monedas["moneda2"]) + (tipos_monedas["moneda3"] * cantidades_monedas["moneda3"])}")
    total_monedas_saldo.place(x=715, y=145)
    #---------------------------------------------------------------------------------------------------
    billetes_saldo_total1 = Label(root, text=f"{tipos_billetes["billete1"] * cantidades_billetes["billete1"]}")
    billetes_saldo_total1.place(x=715, y=180)
    
    billetes_saldo_total2 = Label(root, text=f"{tipos_billetes["billete2"] * cantidades_billetes["billete2"]}")
    billetes_saldo_total2.place(x=715, y=200)
    
    billetes_saldo_total3 = Label(root, text=f"{tipos_billetes["billete3"] * cantidades_billetes["billete3"]}")
    billetes_saldo_total3.place(x=715, y=220)
    
    billetes_saldo_total4 = Label(root, text=f"{tipos_billetes["billete4"] * cantidades_billetes["billete5"]}")
    billetes_saldo_total4.place(x=715, y=240)
    
    billetes_saldo_total5 = Label(root, text=f"{tipos_billetes["billete5"] * cantidades_billetes["billete5"]}")
    billetes_saldo_total5.place(x=715, y=260)
    
    total_billetes_saldo = Label(root, text=f"{((tipos_billetes["billete1"] * cantidades_billetes["billete1"]) - (tipos_billetes["billete1"] * salidas_billetes["billete1"])) + ((tipos_billetes["billete2"] * cantidades_billetes["billete2"]) - (tipos_billetes["billete2"] * salidas_billetes["billete2"])) + ((tipos_billetes["billete3"] * cantidades_billetes["billete3"]) - (tipos_billetes["billete3"] * salidas_billetes["billete3"])) + ((tipos_billetes["billete4"] * cantidades_billetes["billete4"]) - (tipos_billetes["billete4"] * salidas_billetes["billete4"])) + ((tipos_billetes["billete5"] * cantidades_billetes["billete5"]) - (tipos_billetes["billete5"] * salidas_billetes["billete5"]))}")
    total_billetes_saldo.place(x=715, y=285)
    
    monedas_carga1.bind("<KeyRelease>", actualizar_resultado)
    monedas_carga2.bind("<KeyRelease>", actualizar_resultado)
    monedas_carga3.bind("<KeyRelease>", actualizar_resultado)
    billetes_carga1.bind("<KeyRelease>", actualizar_resultado)
    billetes_carga2.bind("<KeyRelease>", actualizar_resultado)
    billetes_carga3.bind("<KeyRelease>", actualizar_resultado)
    billetes_carga4.bind("<KeyRelease>", actualizar_resultado)
    billetes_carga5.bind("<KeyRelease>", actualizar_resultado)

    Button(root, text="Aceptar", command=agregar_carga).place(x=100, y=330)
    Button(root, text="Cancelar", command=mostrar_pagina_inicio).place(x=200, y=330)

#_________________________________________________________ENTRADA DEL VEHÍCULO____________________________________________________________
#[ [placa, numero_espacio, fecha_hora_entrada, fecha_hora_pago, valor_pagado, fecha_hora_salida], … ]

#Función: Entrada de vehículos al estacionamiento
#Entradas: una placa y un boton
#Salidas: se agrega el vehículo a la lista de vehículos o se vuelve al menú principal
def abrir_entrada_vehiculo():
    if existe_configuracion == False:
        error_no_hay_configuracion()
        return

    cantidad_usados = 0
    for campo in parqueo:
        if campo != []:
            cantidad_usados += 1
    if cantidad_usados == len(parqueo):
        error_parqueo_lleno()
        return
    
    limpiar_ventana()
    estacionara = 0
    for espacio, disponible in enumerate(parqueo):
        if disponible == []:
            estacionara = espacio
            break
    titulo_entrada = Label(root, text="ESTACIONAMIENTO - ENTRADA DE VEHÍCULO:", font=("Times New Roman", 14)).place(x=0, y=10)
    titulo_entrada = Label(root, text=f"Espacios disponibles:                 {len(parqueo) - cantidad_usados}").place(x=0, y=35)

    mensaje_espacios = Label(root, text="Placa a ingresar:").place(x=0, y=70)
    
    reg = root.register(validate_placa)
    vehiculo_entry = Entry(root, width=20, validate="key", validatecommand=(reg, '%P'))
    vehiculo_entry.place(x=300, y=70)

    campo_asignado = Label(root, text=f"Campo asignado:                       {estacionara + 1}").place(x=0, y=105)

    tiempo_actual = datetime.now()
    tiempo_entrada = Label(root, text=f"Hora de entrada:            {tiempo_actual.strftime("%H:%M %d-%m-%Y")}").place(x=0, y=140)

    precio_x_hora = Label(root, text=f"Precio por hora:                      {diccionario_configuracion["precio_por_hora"]}").place(x=0, y=175)
    pago_min = Label(root, text=f"Pago mínimo:                          {diccionario_configuracion["pago_minimo"]}").place(x=0, y=210)

    
    def verificar_entrada():
        valido = vehiculo_entry.get()
        if not valido:
            messagebox.showerror("Error", "Debe introducir una placa para añadir un vehículo.")
            return False
        return True
    def borrar_contenido():
        vehiculo_entry.delete(0, END)

    def aceptar_entrada_parqueo():
        for vehiculo in parqueo:
            if vehiculo and vehiculo[0] == str(vehiculo_entry.get()):
                borrar_contenido()
                error_placa_encontrada()
                return

        if verificar_entrada():
            parqueo[estacionara] = [vehiculo_entry.get(), tiempo_actual.strftime('%H:%M %d-%m-%Y')]
        limpiar_ventana()
        abrir_entrada_vehiculo()

    aceptar = Button(root, text="Aceptar", command=aceptar_entrada_parqueo).place(x=100, y=300)
    cancelar = Button(root, text="Cancelar", command=mostrar_pagina_inicio).place(x=200, y=300)

#________________________________________________________________CAJERO__________________________________________________________________
#Función: abrir cajero de pago
#Entradas: Placa de un vehículo, botones para pagar, boton para aceptar el pago
#Salidas: se paga la estadia del vehículo 
def abrir_cajero():
    global a_pagar, pagar, pago, cambio, hora_entrada, hora_salida, tiempo_cobrado, contador, monto_pagar, boton_moneda1, boton_moneda2, boton_moneda3, boton_billete1, boton_billete2, boton_billete3, boton_billete4, boton_billete5, tarjeta_credito, total_horas_pagar, monto_pagar
    if existe_configuracion == False:
        error_no_hay_configuracion()
        return

    elif verificar_parqueo_vacio(parqueo):
        error_parqueo_vacio()
        return
    
    limpiar_ventana()

    def borrar_contenido(entry):
        entry.delete(0, END)

    def revertir_movimientos():
        global a_pagar, pagar, pago, cambio, hora_entrada, hora_salida, tiempo_cobrado, monto_pagar, boton_moneda1, boton_moneda2, boton_moneda3, boton_billete1, boton_billete2, boton_billete3, boton_billete4, boton_billete5, tarjeta_credito, anular
        a_pagar.config(text="A PAGAR")
        pagar.config(text="XXXXXX", font=("Arial", 15))
        pago.config(text=f"Pago:    XXXXX")
        cambio.config(text=f"Cambio:    XXXXX")
        hora_entrada.config(text="HORA DE ENTRADA:        HH:MM     DD/MM/AAAA")
        hora_salida.config(text="HORA DE SALIDA:            HH:MM     DD/MM/AAAA")
        tiempo_cobrado.config(text="TIEMPO COBRADO:         xxH yyM zzzD")
        boton_moneda1.config(state="disabled")
        boton_moneda2.config(state="disabled")
        boton_moneda3.config(state="disabled")
        boton_billete1.config(state="disabled")
        boton_billete2.config(state="disabled")
        boton_billete3.config(state="disabled")
        boton_billete4.config(state="disabled")
        boton_billete5.config(state="disabled")
        tarjeta_credito.config(state="disabled")
        anular.config(state="disabled")

    def check_card_length(entry, vehiculo):
        if len(entry.get()) == 10:
            contador = diccionario_configuracion['precio_por_hora'] * total_horas_pagar
            pago.config(text=f"Pago:    {contador}")
            cambio.config(text="Cambio:    0")
            boton_moneda1.config(state="disabled")
            boton_moneda2.config(state="disabled")
            boton_moneda3.config(state="disabled")
            boton_billete1.config(state="disabled")
            boton_billete2.config(state="disabled")
            boton_billete3.config(state="disabled")
            boton_billete4.config(state="disabled")
            boton_billete5.config(state="disabled")
            tarjeta_credito.config(state="disabled")
            anular.config(state="disabled")
            for indice, carro in enumerate(parqueo):
                if carro and str(carro[0]) == str(vehiculo):
                    indice = parqueo.index(carro) 
                    tiempo = datetime.now()
                    parqueo[indice].append(tiempo.strftime('%H:%M %d-%m-%Y')) 
                    parqueo[indice].append(contador)
                    if len(carro) == 5:
                        del parqueo[indice][2]
            
        else:
            pago.config(text=f"Pago:    XXXXX")
            cambio.config(text="Cambio:    XXXXX")
    
    def dar_cambio(monto_cambio):
        cambio = monto_cambio
        
        llaves_billetes = ['billete1', 'billete2', 'billete3', 'billete4', 'billete5']
        llaves_monedas = ['moneda1', 'moneda2', 'moneda3']
        
        for idx, billete in enumerate(llaves_billetes):
            cantidad = cantidades_billetes[billete]
            valor_billete = tipos_billetes[billete]
            if cantidad <= 0:
                continue
            while cambio >= valor_billete and cantidad > 0:
                cambio -= valor_billete
                cantidad -= 1
                salidas_billetes_temporal[idx] += 1
        
        for idx, moneda in enumerate(llaves_monedas):
            cantidad = cantidades_monedas[moneda]
            valor_moneda = tipos_monedas[moneda]
            if cantidad <= 0:
                continue
            while cambio >= valor_moneda and cantidad > 0:
                cambio -= valor_moneda
                cantidad -= 1
                salidas_monedas_temporal[idx] += 1
                
        if cambio > 0:
            print("No se puede dar el cambio.")
            return None
        else:
            return salidas_billetes_temporal, salidas_monedas_temporal

    def incrementar(valor, buscado):
        global contador, a_pagar, pagar, pago, cambio, hora_entrada, hora_salida, tiempo_cobrado, monto_pagar, boton_moneda1, boton_moneda2, boton_moneda3, boton_billete1, boton_billete2, boton_billete3, boton_billete4, boton_billete5, tarjeta_credito
        if monto_pagar > contador:
            contador += valor
            print(valor)
            pago.config(text=f"Pago:    {contador}")
        if contador >= monto_pagar:
            boton_moneda1.config(state="disabled")
            boton_moneda2.config(state="disabled")
            boton_moneda3.config(state="disabled")
            boton_billete1.config(state="disabled")
            boton_billete2.config(state="disabled")
            boton_billete3.config(state="disabled")
            boton_billete4.config(state="disabled")
            boton_billete5.config(state="disabled")
            tarjeta_credito.config(state="disabled")
            anular.config(state="disabled")
            cambio.config(text=f"Cambio:    {contador - monto_pagar}")
            monto_cambio = contador - monto_pagar
            dar_cambio(monto_cambio)
            cambio_m1.config(text=f"{salidas_monedas_temporal[0]} DE {tipos_monedas['moneda1']}")
            cambio_m1.place(x=135, y=380)
            cambio_m2.config(text=f"{salidas_monedas_temporal[1]} DE {tipos_monedas['moneda2']}")
            cambio_m2.place(x=135, y=410)
            cambio_m3.config(text=f"{salidas_monedas_temporal[2]} DE {tipos_monedas['moneda3']}")
            cambio_m3.place(x=135, y=440)

            cambio_b1.config(text=f"{salidas_billetes_temporal[0]} DE {tipos_billetes['billete1']}")
            cambio_b1.place(x=245, y=380)
            cambio_b2.config(text=f"{salidas_billetes_temporal[1]} DE {tipos_billetes['billete2']}")
            cambio_b2.place(x=245, y=410)
            cambio_b3.config(text=f"{salidas_billetes_temporal[2]} DE {tipos_billetes['billete3']}")
            cambio_b3.place(x=245, y=440)
            cambio_b4.config(text=f"{salidas_billetes_temporal[3]} DE {tipos_billetes['billete4']}")
            cambio_b4.place(x=245, y=470)
            cambio_b5.config(text=f"{salidas_billetes_temporal[4]} DE {tipos_billetes['billete5']}")
            cambio_b5.place(x=245, y=500)

            salidas_monedas["moneda1"] += salidas_monedas_temporal[0]
            salidas_monedas["moneda2"] += salidas_monedas_temporal[1]
            salidas_monedas["moneda3"] += salidas_monedas_temporal[2]
            salidas_billetes["billete1"] += salidas_billetes_temporal[0]
            salidas_billetes["billete2"] += salidas_billetes_temporal[1]
            salidas_billetes["billete3"] += salidas_billetes_temporal[2]
            salidas_billetes["billete4"] += salidas_billetes_temporal[3]
            salidas_billetes["billete5"] += salidas_billetes_temporal[4]
            cantidades_monedas["moneda1"] -= salidas_monedas_temporal[0]
            cantidades_monedas["moneda2"] -= salidas_monedas_temporal[1]
            cantidades_monedas["moneda3"] -= salidas_monedas_temporal[2]
            cantidades_billetes["billete1"] -= salidas_billetes_temporal[0]
            cantidades_billetes["billete2"] -= salidas_billetes_temporal[1]
            cantidades_billetes["billete3"] -= salidas_billetes_temporal[2]
            cantidades_billetes["billete4"] -= salidas_billetes_temporal[3]
            cantidades_billetes["billete5"] -= salidas_billetes_temporal[4]
            for indice, carro in enumerate(parqueo):
                if carro and str(carro[0]) == str(buscado):
                    tiempo = datetime.now()
                    parqueo[indice].append(tiempo.strftime('%H:%M %d-%m-%Y')) 
                    parqueo[indice].append(contador)
                    if len(carro) == 5:
                        del parqueo[indice][2]
    
    def pagar_vehiculo(*arg):
        carro_found = False
        buscado = str(vehiculo_entry.get())
        salidas_monedas_temporal = [0, 0, 0]
        salidas_billetes_temporal = [0, 0, 0, 0, 0]
        for carro in parqueo:
            if carro and str(carro[0]) == buscado:
                if len(carro) == 4:
                    indice_quedados = parqueo.index(carro)
                    time_actual = datetime.now()
                    parqueo[indice_quedados].append(time_actual.strftime('%H:%M %d-%m-%Y'))
                    historial.append(parqueo[indice_quedados])
                    del parqueo[indice_quedados][1]
                    del parqueo[indice_quedados][-1]

                carro_found = True
                global contador, a_pagar, pagar, pago, cambio, hora_entrada, hora_salida, tiempo_cobrado, monto_pagar, boton_moneda1, boton_moneda2, boton_moneda3, boton_billete1, boton_billete2, boton_billete3, boton_billete4, boton_billete5, tarjeta_credito, total_horas_pagar, monto_pagar
                contador = 0

                entrada = datetime.strptime(carro[1], "%H:%M %d-%m-%Y")
                salida = datetime.now()
                diferencia = salida - entrada
                dias = diferencia.days
                horas, resto = divmod(diferencia.seconds, 3600)
                minutos, _ = divmod(resto, 60)
                horas_totales = dias * 24 + horas

                redondear_hasta = int(redondear_minuto.get()) if redondear_minuto.get() else diccionario_configuracion["redondear_minuto"]
                nuevas_horas, nuevos_minutos = ajustar_tiempo(0, minutos, redondear_hasta)
                total_horas_pagar = horas_totales + nuevas_horas
                hora_entrada.config(text=f"HORA DE ENTRADA:        {carro[1]}")
                hora_salida.config(text=f"HORA DE SALIDA:            {salida.strftime('%H:%M %d-%m-%Y')}")
                tiempo_cobrado.config(text=f"TIEMPO COBRADO:          {total_horas_pagar}H   {nuevos_minutos}M   {dias}D")
                monto_pagar = diccionario_configuracion['precio_por_hora'] * total_horas_pagar
                if total_horas_pagar == 0:
                    monto_pagar = diccionario_configuracion["pago_minimo"]
                pagar.config(text=f"{monto_pagar}")

                boton_moneda1.config(state="normal")
                boton_moneda2.config(state="normal")
                boton_moneda3.config(state="normal")
                boton_billete1.config(state="normal")
                boton_billete2.config(state="normal")
                boton_billete3.config(state="normal")
                boton_billete4.config(state="normal")
                boton_billete5.config(state="normal")
                tarjeta_credito.config(state="normal")
                anular.config(state="normal")

        if carro_found == False:
            a_pagar.config(text="A PAGAR")
            pagar.config(text="XXXXXX", font=("Arial", 15))
            pago.config(text=f"Pago:    XXXXX")
            cambio.config(text=f"Cambio:    XXXXX")
            hora_entrada.config(text="HORA DE ENTRADA:        HH:MM     DD/MM/AAAA")
            hora_salida.config(text="HORA DE SALIDA:            HH:MM     DD/MM/AAAA")
            tiempo_cobrado.config(text="TIEMPO COBRADO:         xxH yyM zzzD")
            cambio_m1.config(text=f"{salidas_monedas_temporal[0]} DE {tipos_monedas['moneda1']}")
            cambio_m2.config(text=f"{salidas_monedas_temporal[1]} DE {tipos_monedas['moneda2']}")
            cambio_m3.config(text=f"{salidas_monedas_temporal[2]} DE {tipos_monedas['moneda3']}")

            cambio_b1.config(text=f"{salidas_billetes_temporal[0]} DE {tipos_billetes['billete1']}")
            cambio_b2.config(text=f"{salidas_billetes_temporal[1]} DE {tipos_billetes['billete2']}")
            cambio_b3.config(text=f"{salidas_billetes_temporal[2]} DE {tipos_billetes['billete3']}")
            cambio_b4.config(text=f"{salidas_billetes_temporal[3]} DE {tipos_billetes['billete4']}")
            cambio_b5.config(root, text=f"{salidas_billetes_temporal[4]} DE {tipos_billetes['billete5']}")
            boton_moneda1.config(state="disabled")
            boton_moneda2.config(state="disabled")
            boton_moneda3.config(state="disabled")
            boton_billete1.config(state="disabled")
            boton_billete2.config(state="disabled")
            boton_billete3.config(state="disabled")
            boton_billete4.config(state="disabled")
            boton_billete5.config(state="disabled")
            tarjeta_credito.config(state="disabled")
            anular.config(state="disabled")


    cajero = Label(root, text="CAJERO", font=("Times New Roman", 15, "bold")).place(x=275, y=0)
    monto_x_hora = Label(root, text=f"{diccionario_configuracion['precio_por_hora']} COLONES POR HORA").place(x=450, y=10)
    su_placa = Label(root, text="SU PLACA:").place(x=0, y=40)

    vali_vehiculo = root.register(validate_placa)
    vehiculo_entry = StringVar()
    vehiculo_entry.trace_add("write", pagar_vehiculo)
    vehiculo = Entry(root, textvariable=vehiculo_entry, width=40, validate="key", validatecommand=(vali_vehiculo, '%P'))
    vehiculo.place(x=80, y=40)
    vehiculo.bind("<KeyRelease>", pagar_vehiculo)

    a_pagar = Label(root, text="A PAGAR")
    a_pagar.place(x=350, y=55)
    pagar = Label(root, text="XXXXXX", font=("Arial", 15))
    pagar.place(x=350, y=85)
    pago = Label(root, text=f"Pago:    XXXXX")
    pago.place(x=500, y=75)
    cambio = Label(root, text=f"Cambio:    XXXXX")
    cambio.place(x=500, y=110)
    hora_entrada = Label(root, text="HORA DE ENTRADA:        HH:MM     DD/MM/AAAA")
    hora_entrada.place(x=0, y=65)
    hora_salida = Label(root, text="HORA DE SALIDA:            HH:MM     DD/MM/AAAA")
    hora_salida.place(x=0, y=95)
    tiempo_cobrado = Label(root, text="TIEMPO COBRADO:         xxH yyM zzzD")
    tiempo_cobrado.place(x=0, y=125)
    paso_2 = Label(root, text="SU PAGO EN:                   MONEDAS                           BILLETES                    TARJETA DE CRÉDITO").place(x=0, y=160)
    boton_moneda1 = Button(root, text=f"{tipos_monedas["moneda1"]}", width=10, command=lambda: incrementar(tipos_monedas["moneda1"], vehiculo.get()))
    boton_moneda1.place(x=120, y=190)
    boton_moneda2 = Button(root, text=f"{tipos_monedas["moneda2"]}", width=10, command=lambda: incrementar(tipos_monedas["moneda2"], vehiculo.get()))
    boton_moneda2.place(x=120, y=220)
    boton_moneda3 = Button(root, text=f"{tipos_monedas["moneda3"]}", width=10, command=lambda: incrementar(tipos_monedas["moneda3"], vehiculo.get()))
    boton_moneda3.place(x=120, y=250)
    boton_billete1 = Button(root, text=f"{tipos_billetes["billete1"]}", width=10, command=lambda: incrementar(tipos_billetes["billete1"], vehiculo.get()))
    boton_billete1.place(x=250, y=190)
    boton_billete2 = Button(root, text=f"{tipos_billetes["billete2"]}", width=10, command=lambda: incrementar(tipos_billetes["billete2"], vehiculo.get()))
    boton_billete2.place(x=250, y=220)
    boton_billete3 = Button(root, text=f"{tipos_billetes["billete3"]}", width=10, command=lambda: incrementar(tipos_billetes["billete3"], vehiculo.get()))
    boton_billete3.place(x=250, y=250)
    boton_billete4 = Button(root, text=f"{tipos_billetes["billete4"]}", width=10, command=lambda: incrementar(tipos_billetes["billete4"], vehiculo.get()))
    boton_billete4.place(x=250, y=280)
    boton_billete5 = Button(root, text=f"{tipos_billetes["billete5"]}", width=10, command=lambda: incrementar(tipos_billetes["billete5"], vehiculo.get()))
    boton_billete5.place(x=250, y=310)
    rev_tarjeta = root.register(validate_tarjeta)
    tarjeta_credito = Entry(root, width=15, validate="key", validatecommand=(rev_tarjeta, '%P'))
    tarjeta_credito.place(x=380, y=190)
    tarjeta_credito.bind("<KeyRelease>", lambda event: check_card_length(tarjeta_credito, vehiculo.get()))
    paso_3 = Label(root, text="SU CAMBIO EN:                MONEDAS:                 BILLETES:").place(x=0, y=350)
    cambio_m1 = Label(root, text=f"{salidas_monedas_temporal[0]} DE {tipos_monedas['moneda1']}")
    cambio_m1.place(x=135, y=380)
    cambio_m2 = Label(root, text=f"{salidas_monedas_temporal[1]} DE {tipos_monedas['moneda2']}")
    cambio_m2.place(x=135, y=410)
    cambio_m3 = Label(root, text=f"{salidas_monedas_temporal[2]} DE {tipos_monedas['moneda3']}")
    cambio_m3.place(x=135, y=440)

    cambio_b1 = Label(root, text=f"{salidas_billetes_temporal[0]} DE {tipos_billetes['billete1']}")
    cambio_b1.place(x=245, y=380)
    cambio_b2 = Label(root, text=f"{salidas_billetes_temporal[1]} DE {tipos_billetes['billete2']}")
    cambio_b2.place(x=245, y=410)
    cambio_b3 = Label(root, text=f"{salidas_billetes_temporal[2]} DE {tipos_billetes['billete3']}")
    cambio_b3.place(x=245, y=440)
    cambio_b4 = Label(root, text=f"{salidas_billetes_temporal[3]} DE {tipos_billetes['billete4']}")
    cambio_b4.place(x=245, y=470)
    cambio_b5 = Label(root, text=f"{salidas_billetes_temporal[4]} DE {tipos_billetes['billete5']}")
    cambio_b5.place(x=245, y=500)
    anular = Button(root, text="Anular el pago", command=revertir_movimientos)
    anular.place(x=40, y=550)
    boton_moneda1.config(state="disabled")
    boton_moneda2.config(state="disabled")
    boton_moneda3.config(state="disabled")
    boton_billete1.config(state="disabled")
    boton_billete2.config(state="disabled")
    boton_billete3.config(state="disabled")
    boton_billete4.config(state="disabled")
    boton_billete5.config(state="disabled")
    tarjeta_credito.config(state="disabled")
    anular.config(state="disabled") 
#_________________________________________________________SALIDA DEL VEHÍCULO____________________________________________________________
#Función: salida del vehículo
#Entrada: La placa de un vehículo dentro del estacionamiento
#Salida: Sale el vehículo del estacionamiento, puede indicarle al usuario que se pasó del tiempo de salida. Se modifica el historial del estacionamiento.
def abrir_salida_vehiculo():
    if existe_configuracion == False:
        error_no_hay_configuracion()
        return

    elif verificar_parqueo_vacio(parqueo):
        error_parqueo_vacio()
        return
    limpiar_ventana()
    def verificar_entrada():
        valido = vehiculo_entry.get()
        if not valido:
            messagebox.showerror("Error", "Debe introducir una placa para buscar un vehículo.")
            return False
        return True

    def salida_del_vehiculo(vehiculo):
        if verificar_entrada():
            vehiculo_found = False
            for indice, carro in enumerate(parqueo):
                if carro and carro[0] == vehiculo:
                    vehiculo_found = True
                    if len(carro) == 4:
                        def borrar_contenido():
                            vehiculo_entry.delete(0, END)
                        
                        salida_fisica = datetime.now()
                        salida = datetime.strptime(carro[2], "%H:%M %d-%m-%Y")
                        diferencia = salida_fisica - salida
                        minutos = diferencia.total_seconds() / 60

                        if minutos <= diccionario_configuracion["minutos_maximos_salir"] or diccionario_configuracion["minutos_maximos_salir"] == 0:
                            salida_actual = datetime.now().strftime("%H:%M %d-%m-%Y")
                            parqueo[indice].append(salida_actual)
                            historial.append(parqueo[indice])
                            parqueo[indice] = []
                            borrar_contenido()

                        else:
                            tiempo_sobrepasado(minutos)
                            borrar_contenido()
                    else:
                        messagebox.showerror("Error", "Vehículo no ha pagado, no puede salir.")
                
            if not vehiculo_found:
                messagebox.showerror("Error", "Vehículo no encontrado en el estacionamiento.")
            
    titulo_salida_vehiculo = Label(root, text="ESTACIONAMIENTO - SALIDA DE VEHÍCULO:", font=("Times New Roman", 14)).place(x=0, y=10)
    su_placa = Label(root, text="SU PLACA:").place(x=0, y=40)
    

    reg = root.register(validate_placa)
    vehiculo_entry = Entry(root, width=20, validate="key", validatecommand=(reg, '%P'))
    vehiculo_entry.place(x=80, y=40)
    
    aceptar = Button(root, text="Ok", command=lambda: salida_del_vehiculo(vehiculo_entry.get())).place(x=100, y=80)
    cancelar = Button(root, text="Cancelar", command=mostrar_pagina_inicio).place(x=150, y=80)

#____________________________________________________REPORTE DE INGRESOS DE DINERO_______________________________________________________
#Función: ingresos del dinero
#Entradas: 
#Salidas: Estimación de ingresos del estacionamiento (buscar si los reales tambien)
def abrir_ingresos_dinero():
    if existe_configuracion == False:
        error_no_hay_configuracion()
        return
    limpiar_ventana()
    titulo_salida_vehiculo = Label(root, text="ESTACIONAMIENTO - INGRESOS DE DINERO:", font=("Times New Roman", 14)).place(x=0, y=10)
    ingresos_desde = Label(root, text="Ingresos desde el día:").place(x=0, y=40)
    desde_entry = Entry(root, width=20).place(x= 120, y=40)
    ingresos_hasta = Label(root, text="Hasta el día:").place(x=0, y=70)
    hasta_entry = Entry(root, width=20).place(x= 120, y= 70)

    total_efectivo = Label(root, text="TOTAL DE INGRESOS EN EFECTIVOñ                     XXX.XXX.XXX").place(x=0, y=100)
    total_credito = Label(root, text="TOTAL DE INGRESOS EN POR TARJETA DE CRÉDITO      XXX.XXX.XXX").place(x=0, y=100)
    total = Label(root, text="TOTAL DE INGRESOS DE INGRESOS:                        XXX.XXX.XXX").place(x=0, y=100)

    mensaje = Label(root, text="Para hacer una estimación de ingresos digite la fecha y hora hasta la cual ocupa la estimación:").place(x=0, y=120)
    fechaestimacion = Label(root, text="Fecha de estimación").place(x=100, y=140)
    entryfecha = Entry(root, width=20).place(x=250, y=140)
    horaestimacion = Label(root, text="Hora para la estimación").place(x=100, y=180)
    entryfecha = Entry(root, width=20).place(x=250, y=180)
    estimado = Label(root, text="ESTIMADO DE INGRESOS POR RECIBIR").place(x=0, y=220)

    Button(root, text="Ok").place(x=20, y= 260)
    Button(root, text="Cancelación").place(x=60, y= 260)

#________________________________________________________________AYUDA___________________________________________________________________
#Función: ayuda, obtener manual de usuario
#Entrada: N/A
#Salidas: se le descarga al usuario el manual del usuario
def abrir_ayuda(url):
    webbrowser.open(url)
    mostrar_pagina_principal()
#______________________________________________________________ACERCA DE_________________________________________________________________
#Función: acerca del programa
#Entradas: boton para volver al menú principal
#Salidas: despliega información general del programa
def abrir_acerca_de():
    limpiar_ventana()
    titulo_acerca_de = Label(root, text="ESTACIONAMIENTO - ACERCA DEL PROGRAMA", font=("Times New Roman", 14)).place(x=0, y=10)
    nombre_programa = Label(root, text="Nombre del programa: Estacionamiento de vehículos", font=("Arial", 14)).place(x=0, y=40)
    version = Label(root, text="Versión del programa: 1.0.0", font=("Arial", 14)).place(x=0, y=70)
    fecha_creacion = Label(root, text="Fecha de creación: 1 de junio del 2024", font=("Arial", 14)).place(x=0, y=100)
    nombre = Label(root, text="Nombre del autor: Santiago Valverde", font=("Arial", 14)).place(x=0, y=130)

    Button(root, text="Volver", width=15, command=mostrar_pagina_inicio).place(x=140, y=180)

#__________________________________________________________FUNCIÓN PRINCIPAL_____________________________________________________________
diccionario_configuracion = {} 
existe_configuracion = False

root = Tk()
root.title("Estacionamiento de vehículos")
root.geometry("800x800")

#======================================================FUNCIONES PARA ARCHIVOS=========================================
"""def guardar_configuracion(diccionario, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for clave, valor in diccionario.items():
            archivo.write(f"{clave}: {valor}\n")

def cargar_configuracion(nombre_archivo):
    diccionario = {}
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            clave, valor = linea.strip().split(': ')
            diccionario[clave] = valor
    return diccionario

configuracion_cargada = cargar_configuracion("configuracion.dat")

def crear_archivo_inicial():
    with open('cajero.dat', 'wb') as file:
        pickle.dump(tipos_monedas_inicial, file)
        pickle.dump(cantidades_monedas_inicial, file)
        pickle.dump(tipos_billetes_inicial, file)
        pickle.dump(cantidades_billetes_inicial, file)
        pickle.dump(salidas_monedas_inicial, file)
        pickle.dump(salidas_billetes_inicial, file)

# Función para cargar los datos del archivo .dat
def cargar_datos():
    if not os.path.exists('cajero.dat'):
        crear_archivo_inicial()
    
    # Manejo de archivos corruptos o vacíos
    try:
        with open('cajero.dat', 'rb') as file:
            tipos_monedas = pickle.load(file)
            cantidades_monedas = pickle.load(file)
            tipos_billetes = pickle.load(file)
            cantidades_billetes = pickle.load(file)
            salidas_monedas = pickle.load(file)
            salidas_billetes = pickle.load(file)
        return (tipos_monedas, cantidades_monedas, tipos_billetes, cantidades_billetes, salidas_monedas, salidas_billetes)
    except (EOFError, pickle.UnpicklingError):
        print("Error al leer el archivo. Creando un nuevo archivo con datos iniciales.")
        crear_archivo_inicial()
        return (tipos_monedas_inicial, cantidades_monedas_inicial, tipos_billetes_inicial, cantidades_billetes_inicial, salidas_monedas_inicial, salidas_billetes_inicial)

# Función para guardar los datos en el archivo .dat
def guardar_datos(tipos_monedas, cantidades_monedas, tipos_billetes, cantidades_billetes, salidas_monedas, salidas_billetes):
    with open('cajero.dat', 'wb') as file:
        pickle.dump(tipos_monedas, file)
        pickle.dump(cantidades_monedas, file)
        pickle.dump(tipos_billetes, file)
        pickle.dump(cantidades_billetes, file)
        pickle.dump(salidas_monedas, file)
        pickle.dump(salidas_billetes, file)

# Cargar los datos al iniciar el programa
datos = cargar_datos()
tipos_monedas, cantidades_monedas, tipos_billetes, cantidades_billetes, salidas_monedas, salidas_billetes = datos

# Archivo donde se almacenará la información del parqueo
archivo_parqueo = 'parqueo.dat'

# Función para crear el archivo de parqueo
def crear_archivo_parqueo():
    parqueo = [[], [], []]  # Inicializa parqueo con una lista vacía
    with open(archivo_parqueo, 'wb') as f:
        pickle.dump(parqueo, f)
    print("Archivo de parqueo creado.")

# Función para cargar datos del archivo de parqueo
def cargar_parqueo():
    try:
        with open(archivo_parqueo, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("El archivo de parqueo no existe.")
        return []

# Función para guardar datos en el archivo de parqueo
def guardar_parqueo(parqueo):
    with open(archivo_parqueo, 'wb') as f:
        pickle.dump(parqueo, f)
    print("Datos del parqueo guardados.")

crear_archivo_parqueo()

# Cargar los datos del parqueo
parqueo_actual = cargar_parqueo()

parqueo_actual = cargar_parqueo()


# Archivo donde se almacenará la información del historial de parqueo
archivo_historial = 'parqueo.dat'

# Función para crear el archivo de historial
def crear_archivo_historial():
    historial = [[], [], []]  # Inicializa historial con una lista vacía
    with open(archivo_historial, 'wb') as f:
        pickle.dump(historial, f)
    print("Archivo de historial creado.")

# Función para cargar datos del archivo de historial
def cargar_historial():
    try:
        with open(archivo_historial, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("El archivo de historial no existe.")
        return []

# Función para guardar datos en el archivo de historial
def guardar_historial(historial):
    with open(archivo_historial, 'wb') as f:
        pickle.dump(historial, f)
    print("Datos del historial guardados.")

crear_archivo_historial()

historial_actual = cargar_historial()

historial_actual = cargar_historial()

# Archivo donde se almacenará la información de los ingresos del día
archivo_ingresos = 'ingresos_dia.dat'

# Función para crear el archivo de ingresos del día
def crear_archivo_ingresos():
    ingresos_dia = [[], [], []]  # Inicializa ingresos_dia con una lista vacía
    with open(archivo_ingresos, 'wb') as f:
        pickle.dump(ingresos_dia, f)
    print("Archivo de ingresos del día creado.")

# Función para cargar datos del archivo de ingresos del día
def cargar_ingresos():
    try:
        with open(archivo_ingresos, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("El archivo de ingresos del día no existe.")
        return []

# Función para guardar datos en el archivo de ingresos del día
def guardar_ingresos(ingresos_dia):
    with open(archivo_ingresos, 'wb') as f:
        pickle.dump(ingresos_dia, f)
    print("Datos de los ingresos del día guardados.")

crear_archivo_ingresos()

ingresos_actuales = cargar_ingresos()


ingresos_actuales = cargar_ingresos()
"""
#======================================================================================================================
#__________________________________________________VARIABLES / ESTRUCTURAS / CONSTANTES__________________________________________________
cantidad_espacios = StringVar()
precio_por_hora = StringVar()
pago_minimo = StringVar()
redondear_minuto = StringVar()
minutos_maximos_salir = StringVar()
moneda1 = StringVar()
moneda2 = StringVar()
moneda3 = StringVar()
billete1 = StringVar()
billete2 = StringVar()
billete3 = StringVar()
billete4 = StringVar()
billete5 = StringVar()

carga_moneda1 = IntVar()
carga_moneda2 = IntVar()
carga_moneda3 = IntVar()
carga_billete1 = IntVar()
carga_billete2 = IntVar()
carga_billete3 = IntVar()
carga_billete4 = IntVar()
carga_billete5 = IntVar()

diccionario_configuracion = {}


tipos_monedas = {'moneda1': 0, 'moneda2': 0, 'moneda3': 0}
cantidades_monedas = {'moneda1': 0, 'moneda2': 0, 'moneda3': 0}

tipos_billetes = {'billete1': 0, 'billete2': 0, 'billete3': 0, 'billete4': 0, 'billete5': 0}
cantidades_billetes = {'billete1': 0, 'billete2': 0, 'billete3': 0, 'billete4': 0, 'billete5': 0}

salidas_monedas = {'moneda1': 0, 'moneda2': 0, 'moneda3': 0}
salidas_billetes = {'billete1': 0, 'billete2': 0, 'billete3': 0, 'billete4': 0, 'billete5': 0}

salidas_monedas_temporal = [0, 0, 0]
salidas_billetes_temporal = [0, 0, 0, 0, 0]

vaciar = IntVar()

ingresos_dia = []
parqueo = []
historial = []

#======================================================FUNCIONES PARA ARCHIVOS=========================================
# Función para crear y llenar el archivo con datos iniciales
"""def crear_archivo_inicial():
    with open('cajero.dat', 'wb') as file:
        pickle.dump(tipos_monedas_inicial, file)
        pickle.dump(cantidades_monedas_inicial, file)
        pickle.dump(tipos_billetes_inicial, file)
        pickle.dump(cantidades_billetes_inicial, file)
        pickle.dump(salidas_monedas_inicial, file)
        pickle.dump(salidas_billetes_inicial, file)

# Función para cargar los datos del archivo .dat
def cargar_datos_cajero():
    if not os.path.exists('cajero.dat'):
        crear_archivo_inicial()
    
    # Manejo de archivos vacíos
    try:
        with open('cajero.dat', 'rb') as file:
            tipos_monedas = pickle.load(file)
            cantidades_monedas = pickle.load(file)
            tipos_billetes = pickle.load(file)
            cantidades_billetes = pickle.load(file)
            salidas_monedas = pickle.load(file)
            salidas_billetes = pickle.load(file)
        return (tipos_monedas, cantidades_monedas, tipos_billetes, cantidades_billetes, salidas_monedas, salidas_billetes)
    except (EOFError, pickle.UnpicklingError):
        print("Error al leer el archivo. Creando un nuevo archivo con datos iniciales.")
        crear_archivo_inicial()
        return (tipos_monedas_inicial, cantidades_monedas_inicial, tipos_billetes_inicial, cantidades_billetes_inicial, salidas_monedas_inicial, salidas_billetes_inicial)

# Función para guardar los datos en el archivo .dat
def guardar_datos_cajero(tipos_monedas, cantidades_monedas, tipos_billetes, cantidades_billetes, salidas_monedas, salidas_billetes):
    with open('cajero.dat', 'wb') as file:
        pickle.dump(tipos_monedas, file)
        pickle.dump(cantidades_monedas, file)
        pickle.dump(tipos_billetes, file)
        pickle.dump(cantidades_billetes, file)
        pickle.dump(salidas_monedas, file)
        pickle.dump(salidas_billetes, file)

datos = cargar_datos_cajero()
tipos_monedas, cantidades_monedas, tipos_billetes, cantidades_billetes, salidas_monedas, salidas_billetes = datos

"""
#========================================================================================================================================
#__________________________________________________________FUNCIÓN PRINCIPAL_____________________________________________________________

barra = Menu(root)
root.config(menu=barra)

configuracion = Menu(barra)
barra.add_command(label="Configuración", command=abrir_configuracion)

dinero_cajero = Menu(barra)
barra.add_cascade(label="Dinero del cajero", menu=dinero_cajero)
dinero_cajero.add_command(label="Saldo del cajero", command=abrir_saldo_cajero)
dinero_cajero.add_separator()
dinero_cajero.add_command(label="Cargar cajero", command=abrir_cargar_cajero)

entrada_vehiculo = Menu(barra)
barra.add_command(label="Entrada del vehículo", command=abrir_entrada_vehiculo)

cajero = Menu(barra)
barra.add_command(label="Cajero", command=abrir_cajero)

salida_vehiculo = Menu(barra)
barra.add_command(label="Salida del vehículo", command=abrir_salida_vehiculo)

ingresos_dinero = Menu(barra)
barra.add_command(label="Reporte de ingresos de dinero", command=abrir_ingresos_dinero)

ayuda = Menu(barra)
barra.add_command(label="Ayuda", command=lambda: abrir_ayuda("https://1drv.ms/b/s!AhXi00rBclaGmWr7QEglOAD9QAMW?e=jPWRJj"))

acerca_de = Menu(barra)
barra.add_command(label="Acerca de", command=abrir_acerca_de)

salir = Menu(barra)
barra.add_command(label="Salir", command=quit) #lambda: (guardar_configuracion(diccionario_configuracion, "configuracion.dat"), guardar_parqueo(parqueo_actual), guardar_historial(historial_actual), guardar_datos_cajero(tipos_monedas, cantidades_monedas, tipos_billetes, cantidades_billetes, salidas_monedas, salidas_billetes), root.quit()))

mostrar_pagina_inicio()

#root.protocol("WM_DELETE_WINDOW", lambda: (guardar_configuracion(diccionario_configuracion, "configuracion.dat"), guardar_parqueo(parqueo_actual), guardar_historial(historial_actual), guardar_datos_cajero(tipos_monedas, cantidades_monedas, tipos_billetes, cantidades_billetes, salidas_monedas, salidas_billetes), root.quit()))
root.mainloop()

print(parqueo)