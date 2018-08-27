import urllib2, base64
import xml.etree.ElementTree as ET
import os
import tarfile
import json
import string 
archivo = "0006/BOL_CN_27004_0006.xml"

with open(archivo, 'r') as file:
    tree = ET.parse(file)
    root = tree.getroot()
    num_pregunta = ""
    pregunta = ""
    votos = ""
    opcion = ""
    votosSi = ""
    votosNo = ""
    iter = 0
    salida = '{ "datos":{'
    salidaVal = '{ "valores":{'
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
    with open("test_mpio.json", "w") as dpto:
        dpto.write(salida)
    with open("test_mpioval.json", "w") as dptoval:
        dptoval.write(salidaVal)