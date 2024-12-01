import re

def tipo(row):
    diccionario = {"Netbook": 0, "Notebook": 1, "2 in 1 Convertible": 2, "Ultrabook": 3, "Gaming": 4, "Workstation": 5, "else" : 3}
    row = row["TypeName"] 
    if row in diccionario:
        return diccionario[row]
    else: # Obtenemos la calve del diccionario que definimos con el orden de medianas ascendente, si no está allí rellena con el valor medio
        return diccionario["else"] 

def limpia_peso(row):
    row = float(row["Weight"].replace("kg", "")) # Limpiamos las letras de kilogramos en la columan de Weight
    return row

def resolucion(row):
    diccionario = {"1440x900": 1, "1600x900": 2, "1920x1080": 3, "1920x1200": 4, # De nuevo definimos diccionario con las gamas,
                    "2160x1440": 5,"2256x1504": 6, "2304x1440": 7, "2400x1600": 8, "2560x1440": 9, # si no existe rellenamos con valor medio
                    "2560x1600": 10, "2880x1800": 11, "3200x1800": 12, "3840x2160": 13, "else" : 5}  
    data = row["ScreenResolution"]
    patron = re.compile(r"\d{3,4}x\d{3,4}") # Buscamos la forma (alto)x(ancho) de la columna ScreenResolution con una expresión regular
    match = patron.finditer(data)
    for i in match:
        row = i.group()
        break
    if row in diccionario:
        return diccionario[row] # Buscamos la clave en el diccionario
    else:
        return diccionario["else"]

def sistema(row):
    diccionario = {"No OS": 1, "Linux": 2, "Windows 10": 3, "Mac OS X": 4, # De nuevo definimos diccionario con las gamas,
                    "Windows 10 S": 5,"Windows 7": 6, "Mac OS X": 7, "else" : 3} # si no existe rellenamos con valor medio
    row = row["OpSys"]
    if row in diccionario:
        return diccionario[row]
    else:
        return diccionario["else"]

def ram(row):
    row = int(row["Ram"].replace("GB", "")) # Limpiamos las letras de GigaBytes en la columan de RAM
    return row

def regex_cpu(texto, tipo):
    if tipo == "Pentium" or tipo == "Celeron": # Buscamos la forma (gama, generacion, modelo) de la columna CPU con una expresión regular
        string = fr"Intel {tipo} (Quad|Dual) Core\.?\s\w*" # Si es Pentium o Celeron
        patron = re.compile(string)
        match = patron.finditer(texto)
        for i in match:
            y = i.group() 
        try:
            int(y[-4:])
            if int(y[-4:]) > 3350: # Filtramos por modelo y por generacion 
                row = 2
            else:
                row = 1 # Depende de estos ponderamos más o menos
        except:
            if int(y[-5:-1]) > 3350:
                row = 2
            else:
                row = 1
        if tipo == "Pentium":
            row += 1

    elif tipo == "M":
        string = r"Intel Core M\.?\s\w*" # Si es Core M
        patron = re.compile(string)
        match = patron.finditer(texto)
        for i in match:
            y = i.group()
        if y[-6:-4] == "M 6" or y[-6:-4] == "M 7": # Filtramos por modelo y por generacion 
            row = 4                                # Depende de estos ponderamos más o menos
        else:
            row = 5

    elif tipo == "i":
        string = r"Intel Core i\d{1}\.?\s\w*" # Si es Core i
        patron = re.compile(string)
        match = patron.finditer(texto)
        row = 8
        for m in match:
            y = m.group()
        if int(y[14]) in range(0, 7):
            # Filtramos por modelo y por generacion
            # Depende de estos ponderamos más o menos
            if int(y[12]) == 3:       
                row = 6
            elif int(y[12]) == 5 or int(y[12]) == 7:
                row = 7
        elif int(y[14]) in range(8, 12):
            # Si es i3
            if int(y[12]) == 3:
                row = 6
            # Si es i5
            elif int(y[12]) == 5: 
                row = 7
            # Si es i7 o i9
            elif int(y[12]) >= 7: 
                row = 8
    return row

def cpu(row):
    i = row["Cpu"]
    if "Intel" in i: # Ponderamos por gamas tanto de Intel como AMD, las gamams de peor calidad como Intel Atom las ponemos a 0 directamente
        if "Atom" in i: # Y las de gama máxima como Intel Xeon con la máxima directamente, apra el resto lo que devuelva la funcion regex_cpu
            row = 0
        elif "Celeron" in i:
            row = regex_cpu(i, "Celeron")

        elif "Pentium" in i:
            row = regex_cpu(i, "Pentium")

        elif "Core M" in i:
            row = regex_cpu(i, "M")

        elif "Core i" in i:
            row = regex_cpu(i, "i")

        elif "Xeon E" in i:
            row = 9

    elif "AMD" in i:   # Las AMD al no ser tan comunes las clasificamoss directamente escalando las gamas a sus homólogas de Intel
        if "E-Series" in i:
            row = 0

        if "AMD A" in i:
            row = 2

        if "AMD FX " in i:
            row = 4

        if "Ryzen" in i:
            row = 7
    elif "Samsung Cortex" in i:
        row = 4
    return row

def almacenamiento(row): # Hacemos un split de la columna Memory para sacar la capacidad de almacenamiento del ordenador
    row = row["Memory"]  # Sumamos los espacios de los discos duros en caso de que el ordenador tenga dos
    x = row.split()
    if (len(x) < 3) or (len(x) == 3 and "Flash" in x):
        if "TB" in x[0]:
            row = int(x[0][0]) * 1024
        else:
            row = int(x[0].replace("GB", ""))
    elif len(x) > 3:
        la_0 = x[0]
        if "TB" in la_0:
            primero = int(la_0[0]) * 1024
        else:
            primero = la_0[0].replace("GB", "")
        la_1 = x[-2]
        if "TB" in la_1:
            segundo = int(la_1[0]) * 1024
        else:
            segundo = la_1[0].replace("GB", "")
        row = int(primero) + int(segundo)
    return row

def almacenamiento_tipo(row):
    diccionario = {"Flash" : 0, "Storage" : 0, "HDD" : 1, "Hybrid" : 2, "SSD" : 3}
    row = row["Memory"] # Hacemos un split de la columna Memory para sacar la capacidad de almacenamiento del ordenador
    x = row.split()     # Separamos por gamas siendo Flash Storage la peor y SSD la mejor
    if len(x) <= 3:     # Busca los valores de cada uno en el diccionario de arriba y los suma en el caso de que sean dos discos duros
        if x[1] in diccionario:
            row = diccionario[x[1]] 

    elif len(x) > 3:
        if x[1] in diccionario:
            row_ = diccionario[x[1]]

        if x[1] in diccionario:
            row = diccionario[x[-1]]

        row = row_ + row
    return row

def company(row):
    diccionario = {"Acer" : 6, "Apple" : 13, "Asus" : 11, "Chuwi" : 1, "Dell" : 10, "Fujitsu" : 7, "Google" : 15, "HP" : 9, "Huawei" : 17,
                    "LG" : 18, "Lenovo" : 8, "MSI" : 16, "Mediacom" : 12, "Microsoft" : 14, "Razer" : 19, "Samsung" :17, "Toshiba" : 12,
                    "Vero" : 2, "Xiamoi" : 13} 
    row = row["Company"] # Ponderamos por el fabricante, de nuevo las medianas más altas tienen más ponderación, si están muy juntas
    if row in diccionario: # son ponderados como iguales
        return diccionario[row]
    else:
        return 9

def potencia(row): # Hacemos un split de la columna CPU y extraemos la frecuencia/potencia del mismo
    row = row["Cpu"]
    return float(row.split()[-1].replace("GHz", ""))