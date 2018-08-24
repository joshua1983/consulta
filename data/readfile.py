import urllib2, base64
import xml.etree.ElementTree as ET
import os
import tarfile
import json
import string 
archivo = "0008/BOL_CN_DE000_0008.xml"

with open(archivo, 'r') as file:
    tree = ET.parse(file)
    root = tree.getroot()
    salida = '{ "datos":{'
    for child in root.iter('Boletin'):
        # boletin por departamento
        for data in child:
            if data.tag == 'Departamento':
                salida += '"' + data.attrib.get("V") + '":{'
            for pregunta in data.iter('Detalle_Pregunta'):
                #Armado por cada pregunta
                num_pregunta = 0
                for data_pregunta_lin in pregunta.iter("lin"):
                    for data_pregunta in data_pregunta_lin:
                        if data_pregunta.tag == 'Pregunta':
                            salida += '"'+data_pregunta.attrib.get("V")+'":{'
                        else:
                            if data_pregunta.tag == 'Porc_Votos_Nulos':
                                salida += '"'+data_pregunta.tag+'":"'+data_pregunta.attrib.get("V")+'"'
                            else:
                                salida += '"'+data_pregunta.tag+'":"'+data_pregunta.attrib.get("V")+'",'
                    salida += "},"
                salida = string.replace(salida, "},}", "}}");
                salida = string.replace(salida, "},}", "}}");
    salida += '}'
    print salida