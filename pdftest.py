#!/usr/bin/env python3


#[0-9]{1,2}\.

import re
import os
from utils import log, warning, bold

preguntas = {}
respuestas = {}
soluciones = {}
respuestas_usuario = {}
preguntas_fallidas = []

def parsear_fichero(fichero_test):

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "tests/" + fichero_test
    abs_file_path = os.path.join(script_dir, rel_path)

    # path = "tema11test3.txt"
    log_file = open(abs_file_path, 'r')

    question_mode = False
    answer_mode = False
    current_question = ""
    solution_mode = False
    for line in log_file.readlines():

        if re.match("SOLUCIONES", line):
            solution_mode = True
            continue

        if solution_mode is False:
            question_match = re.match("[0-9]{1,2}[\.\)]{1,1} ", line)
            if question_match:
                current_question = question_match.group().replace(". ", "")
                current_question = current_question.replace(") ", "")
                #print("Line -> " + current_question + " -> " + line)
                preguntas[current_question] = line
                question_mode = True
                answer_mode = False
                continue

            if re.match("[a-dA-D][\.\)] ", line):
                #print("Respuesta: current_question: " + current_question + " -> " + line)
                if current_question not in respuestas:
                    answer_list = []
                    answer_list.append(line)
                    respuestas[current_question] = answer_list
                else:
                    #print("elsito")
                    #print(respuestas[current_question])
                    respuestas[current_question].append(line)
                #print(respuestas[current_question])
                question_mode = False
                answer_mode = True
                continue
            if question_mode is True:
                #print("qmode -> " + line)
                preguntas[current_question] = preguntas[current_question] + line
                continue
            if answer_mode is True:
                #print("amode -> " + line)
                respuestas[current_question][len(respuestas[current_question])-1] = \
                    respuestas[current_question][len(respuestas[current_question])-1] + line
                continue

        else:
            # Parse solutions
            #print("Parsing solution")
            #print(line.split())
            soluciones[line.split()[0]] = line.split()[1]
            #print(soluciones)


def correccion():
    nota = 0
    total_preguntas = len(preguntas)
    valor_pregunta = 10 / total_preguntas

    for clave, pregunta in preguntas.items():
        if respuestas_usuario[clave].lower() == "z":
            # Pregunta sin respuesta
            print(clave + " No Contestada")
            continue
        if soluciones[clave].lower() == respuestas_usuario[clave].lower():
            print(clave + " Acierto")
            nota = nota + valor_pregunta
        else:
            print(clave + " Fallo " + respuestas_usuario[clave].lower() + " -> " + soluciones[clave].lower())
            nota = nota - (valor_pregunta/2)
            preguntas_fallidas.append(clave)

    print("Tu nota es: " + str(nota))


def repaso():
    for clave, pregunta in preguntas.items():
        bold(pregunta)
        for respuesta in respuestas[clave]:
            if re.match("^[" + soluciones[clave].lower() + "]+", respuesta.lower()):
                warning(respuesta)
            else:
                print(respuesta)
        print("")
        input("Pulsa Enter para continuar")
        print("\n\n\n")



def repasar_fallos():
    print(preguntas_fallidas)
    for clave in preguntas_fallidas:
        bold(preguntas[clave])
        for respuesta in respuestas[clave]:
            if re.match("^[" + soluciones[clave].lower() + "]+", respuesta.lower()):
                warning(respuesta)
            else:
                print(respuesta)
        print("")
        input("Pulsa Enter para continuar")
        print("\n\n\n")


def uno_a_uno():
    # Empieza el test al usuario
    for clave, pregunta in preguntas.items():
        bold(pregunta)
        for respuesta in respuestas[clave]:
            print(respuesta)
        respuesta_usuario = str(input("Respuesta:").lower().strip())
        while not re.match("^[abcdez]{1,1}$", respuesta_usuario):
            respuesta_usuario = str(input("Respuesta:").lower().strip())
        respuestas_usuario[clave] = respuesta_usuario

        # Comprobar la respuesta sobre la marcha
        if respuestas_usuario[clave].lower() == "z":
            # Pregunta sin respuesta
            print(clave + " No Contestada " + " la correcta es la '" + soluciones[clave].lower() + "'")
        elif soluciones[clave].lower() == respuestas_usuario[clave].lower():
            print(clave + " Acierto!!!")
        else:
            print(clave + " Fallo. Pusiste '" + respuestas_usuario[clave].lower() +
                  "' la correcta es '" + soluciones[clave].lower() + "'")
        print("")
        input("Pulsa Enter para continuar")
        print("\n\n\n")

    print("Fin del test. Correccion:")
    correccion()

    respuesta_usuario = str(input("¿quieres repasar los fallos? (y/n):").lower().strip())
    while not re.match("^[yn]+$", respuesta_usuario):
        respuesta_usuario = str(input("¿quieres repasar los fallos? (y/n):").lower().strip())

    if respuesta_usuario == "y":
        repasar_fallos()

def examen():
    # Empieza el test al usuario
    for clave, pregunta in preguntas.items():
        bold(pregunta)
        for respuesta in respuestas[clave]:
            print(respuesta)
        respuesta_usuario = str(input("Respuesta:").lower().strip())
        while not re.match("^[abcdez]{1,1}$", respuesta_usuario):
            respuesta_usuario = str(input("Respuesta:").lower().strip())
        respuestas_usuario[clave] = respuesta_usuario
        print("\n\n\n")

    print("Fin del test. Correccion:")
    correccion()

    respuesta_usuario = str(input("¿quieres repasar los fallos? (y/n):").lower().strip())
    while not re.match("^[yn]+$", respuesta_usuario):
        respuesta_usuario = str(input("¿quieres repasar los fallos? (y/n):").lower().strip())

    if respuesta_usuario == "y":
        repasar_fallos()

def validar_test():
    if len(preguntas) != len(soluciones):
        print("pero tiene " + str(len(soluciones)) + " soluciones, hay algo raro")
        respuesta_usuario = ""
        while not re.match("^[yn]+$", respuesta_usuario):
            respuesta_usuario = str(input("¿quieres hacer el test de todas formas? (y/n):").lower().strip())
        if respuesta_usuario == "n":
            exit(0)

def principal():

    print("Heyyyyy")
    modo = input("¿Que modo quieres? (examen,repaso,one):")
    tema = input("¿Que tema deseas probar?:")

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "tests/"
    abs_file_path = os.path.join(script_dir, rel_path)

    for file in os.listdir(abs_file_path):
        if file.startswith("tema" + tema + "test"):
            print(file)

    test = input("¿Que test del tema " + tema + "?:")
    fichero_test = "tema" + tema + "test" + test + ".txt"
    parsear_fichero(fichero_test)

    print("\n\n\n")
    print("Este test tiene " + str(len(preguntas)) + " preguntas")
    validar_test()
    print("\n\n\n")

    if modo == "repaso":
        repaso()
    elif modo == "one":
        uno_a_uno()
    else:
        examen()

    print("Fin del test")


principal()

# Cosas que faltan:
# Tema 28 Test Mezclados 1 no se puede parsear, es imagen.
# Tema 28 Ademas hay muchisimos mas tests dentro de las carpetas de la ley!!
# Tema 25 monton de tests en la carpeta de actualización al nuevo estatuto por partes
# Tema 24 EBEP test 312 preguntas
# TESTs extra del tema 20,21,22 ¡¡son montones!!
# TESTs extra del tema 13 test ley transparencia canaria (no creo que valga la pena)
# Tema 1 Falta por meter Test extra titulo preliminar
