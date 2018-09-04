import urllib2, base64
import xml.etree.ElementTree as ET
import os
import tarfile
import json
import string 
import re

"""

Funciones de procesamiento de archivos

"""

def procesarNacional(file):
    print "Procesando Nacional: " +file
    with open(file,"r") as file:
        tree = ET.parse(file)
        root = tree.getroot()
        for child in root.iter('Boletin'):
            estadisticas_str = '{"boletin":0, "potsuf":0, "porcmesas":0, "hora":""}'
            estadisticas = json.loads(estadisticas_str)
            datos_preguntas_str = '{"pregunta1": {"votosno":0,"votossi":0, "votosvalidos":0},"pregunta2": {"votosno":0,"votossi":0,"votosvalidos":0},"pregunta3": {"votosno":0,"votossi":0,"votosvalidos":0},"pregunta4": {"votosno":0,"votossi":0,"votosvalidos":0},"pregunta5": {"votosno":0,"votossi":0,"votosvalidos":0},"pregunta6": {"votosno":0,"votossi":0,"votosvalidos":0},"pregunta7": {"votosno":0,"votossi":0,"votosvalidos":0}}'
            datos_preguntas = json.loads(datos_preguntas_str)
            for data in child:
                # Armado de las estadisticas nacionales
                if data.tag == 'Numero':
                    boletin = data.attrib.get("V")
                    estadisticas["boletin"] = boletin
                if data.tag == 'Potencial_Sufragantes':
                    pot_suf = data.attrib.get("V")
                    estadisticas["potsuf"] = pot_suf
                if data.tag == 'Porc_Mesas_Informadas':
                    porc_mesas = data.attrib.get("V")
                    estadisticas["porcmesas"] = porc_mesas
                if data.tag == 'Hora':
                    hora = str(data.attrib.get("V"))
                if data.tag == 'Minuto':
                    hora = hora + ":" + str(data.attrib.get("V"))
                    estadisticas["hora"] = hora
                for pregunta in data.iter('Detalle_Pregunta'):
                    #Armado por cada pregunta
                    num_pregunta = 0
                    for data_pregunta_lin in pregunta.iter("lin"):
                        for data_pregunta in data_pregunta_lin:
                            if data_pregunta.tag == 'Pregunta':
                                num_pregunta = data_pregunta.attrib.get("V")
                            if data_pregunta.tag == 'Votos_Validos':
                                if num_pregunta == '001':
                                    datos_preguntas["pregunta1"]["votosvalidos"] = data_pregunta.attrib.get("V")
                                if num_pregunta == '002':
                                    datos_preguntas["pregunta2"]["votosvalidos"] = data_pregunta.attrib.get("V")
                                if num_pregunta == '003':
                                    datos_preguntas["pregunta3"]["votosvalidos"] = data_pregunta.attrib.get("V")
                                if num_pregunta == '004':
                                    datos_preguntas["pregunta4"]["votosvalidos"] = data_pregunta.attrib.get("V")
                                if num_pregunta == '005':
                                    datos_preguntas["pregunta5"]["votosvalidos"] = data_pregunta.attrib.get("V")
                                if num_pregunta == '006':
                                    datos_preguntas["pregunta6"]["votosvalidos"] = data_pregunta.attrib.get("V")
                                if num_pregunta == '007':
                                    datos_preguntas["pregunta7"]["votosvalidos"] = data_pregunta.attrib.get("V")
                for detalle_pregunta in data.iter('Detalle_Opcion'):
                    for data_pregunta_lin in detalle_pregunta.iter('lin'):

                        #datos de la opcion lin
                        pregunta = ""
                        opcion = ""
                        votos = 0
                        for data_pregunta in data_pregunta_lin:
                            if data_pregunta.tag == 'Pregunta':
                                pregunta = data_pregunta.attrib.get("V")
                            if data_pregunta.tag == 'Opcion':
                                opcion = data_pregunta.attrib.get("V")
                            if data_pregunta.tag == 'Votos':
                                votos = data_pregunta.attrib.get("V")
                        
                        if pregunta == '001':
                            if opcion == '001':
                                # votos por el si
                                datos_preguntas["pregunta1"]["votossi"] = votos
                            else:
                                datos_preguntas["pregunta1"]["votosno"] = votos
                        if pregunta == '002':
                            if opcion == '001':
                                # votos por el si
                                datos_preguntas["pregunta2"]["votossi"] = votos
                            else:
                                datos_preguntas["pregunta2"]["votosno"] = votos
                        if pregunta == '003':
                            if opcion == '001':
                                # votos por el si
                                datos_preguntas["pregunta3"]["votossi"] = votos
                            else:
                                datos_preguntas["pregunta3"]["votosno"] = votos
                        if pregunta == '004':
                            if opcion == '001':
                                # votos por el si
                                datos_preguntas["pregunta4"]["votossi"] = votos
                            else:
                                datos_preguntas["pregunta4"]["votosno"] = votos
                        if pregunta == '005':
                            if opcion == '001':
                                # votos por el si
                                datos_preguntas["pregunta5"]["votossi"] = votos
                            else:
                                datos_preguntas["pregunta5"]["votosno"] = votos
                        if pregunta == '006':
                            if opcion == '001':
                                # votos por el si
                                datos_preguntas["pregunta6"]["votossi"] = votos
                            else:
                                datos_preguntas["pregunta6"]["votosno"] = votos
                        if pregunta == '007':
                            if opcion == '001':
                                # votos por el si
                                datos_preguntas["pregunta7"]["votossi"] = votos
                            else:
                                datos_preguntas["pregunta7"]["votosno"] = votos
    datos_estadisticas_nac =  '{ "estadisticas": '+ json.dumps(estadisticas)+ ', "preguntas": ' + json.dumps(datos_preguntas) +'}'
    os.chdir("..")
    with open("nacional.json", "w") as nac:
        nac.write(datos_estadisticas_nac)

"""

Funcion de procesamiento de archivos departamentales por departamento

"""

def procesarDepartamental(archivo):
    print "Procesando Departamental: " +os.path.abspath(archivo)
    with open(archivo, 'r') as file:
        tree = ET.parse(file)
        root = tree.getroot()
        num_pregunta = ""
        pregunta = ""
        votos = ""
        opcion = ""
        votosSi = ""
        votosNo = ""
        salida = '{ "datos":{'
        salidaVal = '{ "valores":{'
        for child in root.iter('Boletin'):
            # boletin por departamento
            for data in child:
                if data.tag == 'Departamento':
                    salida += '"' + data.attrib.get("V") + '":{'
                    salidaVal += '"' + data.attrib.get("V") + '":{'
                for pregunta in data.iter('Detalle_Pregunta'):
                    #Armado por cada pregunta
                    num_pregunta = ""
                    for data_pregunta_lin in pregunta.iter("lin"):
                        for data_pregunta in data_pregunta_lin:
                            if data_pregunta.tag == 'Pregunta':
                                salida += '"'+data_pregunta.attrib.get("V")+'":{'
                                num_pregunta = data_pregunta.attrib.get("V")
                            else:
                                if data_pregunta.tag == 'Porc_Votos_Nulos':
                                    salida += '"'+data_pregunta.tag+'":"'+data_pregunta.attrib.get("V")+'"'
                                    if num_pregunta == '007':
                                        salida += "}"
                                else:
                                    salida += '"'+data_pregunta.tag+'":"'+data_pregunta.attrib.get("V")+'",'
                        salida += "},"
                    salida = string.replace(salida, "},}", "}}")
                    salida = string.replace(salida, "},}", "}}")
                # cargar los valores de cada pregunta para el departamento            
                preguntaVal = ""

                for valores in data.iter('Detalle_Opcion'):
                    #Armado por cada pregunta
                    for data_pregunta_lin in valores.iter("lin"):
                        preguntaLin = preguntaVal
                        for data_pregunta in data_pregunta_lin:
                            #datos de la opcion lin  
                            if data_pregunta.tag == 'Pregunta':
                                preguntaVal = data_pregunta.attrib.get("V")
                                if preguntaLin == '':
                                    preguntaLin = preguntaVal
                                if preguntaVal == preguntaLin and votosNo != '':
                                    salidaVal += '"'+str(preguntaLin)+'":{"si":"'+votosSi+'","no":"'+votosNo+'"},'
                                    votosSi = ""
                                    votosNo = ""
                                    opcion = ""
                                else:
                                    preguntaLin = preguntaVal     
                            if data_pregunta.tag == 'Opcion':
                                opcion = data_pregunta.attrib.get("V")
                            if data_pregunta.tag == 'Votos':
                                votos = data_pregunta.attrib.get("V")
                                if opcion == '001':
                                    votosSi = votos
                                if opcion == '002':
                                    votosNo = votos
                    salidaVal += "},"
        salidaVal += '}}'
        salidaVal = string.replace(salidaVal, "},}", "}}")
        salidaVal = string.replace(salidaVal, "},}", "}}")
        with open("dpto.json", "w") as dpto:
            salida = string.replace(salida, "},}", "}}") + '}}'
            salida = string.replace(salida, "},}", "}}")
            dpto.write(salida)
        with open("dptoval.json", "w") as dptoval:
            dptoval.write(salidaVal)

"""

Funcion de procesamiento de archivos Capitales

"""
def procesarCapital(boletin):
    
    os.chdir(os.getcwd()+'/'+boletin)
    salida = ''
    print "Procesando capitales para: "+boletin
    patronSantander = re.compile('BOL_CN_27[0-9][0-9][0-9]_'+boletin+'.xml')
    for archivo in os.listdir('.'):
        #procesa datos para santander
        if patronSantander.match(archivo):
            with open(archivo, 'r') as file:
                tree = ET.parse(file)
                root = tree.getroot()
                num_pregunta = ""
                pregunta = ""
                votos = ""
                opcion = ""
                votosSi = ""
                votosNo = ""
                codigoCap = os.path.basename(archivo)
                codCap = codigoCap[9:12]
                salida += ' "datos'+codCap+'":{'
                salidaVal = ' "valores'+codCap+'":{'
                for child in root.iter('Boletin'):
                    # boletin por departamento
                    for data in child:
                        if data.tag == 'Municipio':
                            salida += '"' + data.attrib.get("V") + '":{'
                            salidaVal += '"' + data.attrib.get("V") + '":{'
                        for pregunta in data.iter('Detalle_Pregunta'):
                            #Armado por cada pregunta
                            num_pregunta = ""
                            for data_pregunta_lin in pregunta.iter("lin"):
                                for data_pregunta in data_pregunta_lin:
                                    if data_pregunta.tag == 'Pregunta':
                                        salida += '"'+data_pregunta.attrib.get("V")+'":{'
                                        num_pregunta = data_pregunta.attrib.get("V")
                                    else:
                                        if data_pregunta.tag == 'Porc_Votos_Nulos':
                                            salida += '"'+data_pregunta.tag+'":"'+data_pregunta.attrib.get("V")+'"'
                                            if num_pregunta == '007':
                                                salida += "}"
                                        else:
                                            salida += '"'+data_pregunta.tag+'":"'+data_pregunta.attrib.get("V")+'",'
                                salida += "},"
                                salida = string.replace(salida, "},}", "}}")

                        # cargar los valores de cada pregunta para el departamento            
                        preguntaVal = ""
                        for valores in data.iter('Detalle_Opcion'):
                            #Armado por cada pregunta
                            for data_pregunta_lin in valores.iter("lin"):
                                preguntaLin = preguntaVal
                                for data_pregunta in data_pregunta_lin:
                                    #datos de la opcion lin  
                                    if data_pregunta.tag == 'Pregunta':
                                        preguntaVal = data_pregunta.attrib.get("V")
                                        if preguntaLin == '':
                                            preguntaLin = preguntaVal
                                        if preguntaVal == preguntaLin and votosNo != '':
                                            salidaVal += '"'+str(preguntaLin)+'":{"si":"'+votosSi+'","no":"'+votosNo+'"},'
                                            votosSi = ""
                                            votosNo = ""
                                            opcion = ""
                                        else:
                                            preguntaLin = preguntaVal     
                                    if data_pregunta.tag == 'Opcion':
                                        opcion = data_pregunta.attrib.get("V")
                                    if data_pregunta.tag == 'Votos':
                                        votos = data_pregunta.attrib.get("V")
                                        if opcion == '001':
                                            votosSi = votos
                                        if opcion == '002':
                                            votosNo = votos
                            salidaVal += "},"
                salidaVal += '}}'
                salidaVal = string.replace(salidaVal, "},}", "}}")
                salida = salida + salidaVal
                salida = string.replace(salida, "},}", "}}") + ","
    retorno = '{"data":{' + string.replace(salida, "},}", "}}") + '}}'
    writeFile = string.replace(retorno, "},}", "}}")
    os.chdir('../')
    with open("capitales.json", "w") as cap:
        cap.write(writeFile)



# Url index de los archivos
urlIndex = "https://descargasconsulta2018.registraduria.gov.co/c99descargas/DEPLINDEX.xml"

""" 

	Autorizacion para descargar  COLOCAR USUARIO Y CONTRASEÑA

"""
base64String = base64.b64encode('%s:%s' % ("",""))

request = urllib2.Request(urlIndex)
request.add_header("Authorization", "Basic %s" % base64String)

# Leer el index XML y descargar todos los boletines
xmlIndex = urllib2.urlopen(request)

tree = ET.parse(xmlIndex)
root = tree.getroot() # root = <Avance> 

i=0
boletin = ''
for dpto in root:
    if i==1:
        boletin = dpto.text
        if not os.path.exists(boletin):
            with open("boletin.json", "w") as bol:
                bol.write(boletin)
            os.mkdir(boletin, 0o777)
    if i>1:
        urlDownload = dpto.text
        nombreArchivo = urlDownload.split('/')[-1]
        url = "https://descargasconsulta2018.registraduria.gov.co" + str(urlDownload)
        print("Descargando: "+nombreArchivo)
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % base64String)
        fileData = urllib2.urlopen(request)
        datatowrite = fileData.read()
        archivoTarGZ = os.path.join( boletin,nombreArchivo)
        with open(os.path.join(boletin,nombreArchivo), 'wb') as f:
            f.write(datatowrite)
        #Descomprimir el archivo
        tarZip = tarfile.open(archivoTarGZ)
        tarZip.extractall(boletin)
    i=i+1
print "Procesando boletin: "+str(boletin)
os.chdir(boletin)
path = os.getcwd() + "/"
for file in os.listdir('.'):
    #procesa datos a nivel nacional
    if file == "BOL_CN_00000_"+boletin+".xml" :
        procesarNacional(path+file)
    #procesa datos departamentales
    if file == "BOL_CN_DE000_"+boletin+".xml":
        procesarDepartamental(path+file)
#procesa datos para santander
procesarCapital(boletin)
    
