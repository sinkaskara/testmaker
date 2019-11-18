#!/usr/bin/env python3


#[0-9]{1,2}\.

import re
import os
import datetime
from utils import warning, bold
from utils import load_dict_from_file, save_dict_to_file

ruta_tests = "tests/"
ruta_saves = "saves/"

def log_test(fecha_inicio, fecha_fin, tema, test, modo, preguntas, soluciones, respuestas_usuario):
    try:
        duracion_test = fecha_fin - fecha_inicio
        print("Duracion test: {}".format(duracion_test))

        script_dir = os.path.dirname(__file__) # <-- absolute dir the script is in
        abs_file_path = os.path.join(script_dir, "history.log")
        f = open(abs_file_path, "a")
        if modo == "repaso":
            aciertos = 0
            fallos = 0
            no_contestadas = 0
        else:
            aciertos, fallos, no_contestadas = correccion_silenciosa(preguntas, soluciones, respuestas_usuario)

        f.write("\n"
                + fecha_inicio.strftime('%Y-%m-%d %H:%M:%S') + ";"
                + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ";"
                + '{}'.format(duracion_test) + ";"
                + modo + ";"
                + tema + ";"
                + test + ";"
                + str(len(soluciones)) + ";"
                + str(aciertos) + ";"
                + str(fallos) + ";"
                + str(no_contestadas) + ";"
                + str(respuestas_usuario))
    except Exception as error:
        print("Hubo un problema logueando, no pasa nada, continuamos")
        print(error)

def parsear_fichero(fichero_test):

    script_dir = os.path.dirname(__file__) # <-- absolute dir the script is in
    rel_path = ruta_tests + fichero_test
    abs_file_path = os.path.join(script_dir, rel_path)

    # path = "tema11test3.txt"
    log_file = open(abs_file_path, 'r', encoding='utf-8')

    preguntas_parseo = {}
    respuestas_parseo = {}
    soluciones_parseo = {}

    question_mode = False
    answer_mode = False
    current_question = ""
    solution_mode = False
    for line in log_file.readlines():

        if re.match("SOLUCIONES", line):
            solution_mode = True
            continue

        if solution_mode is False:
            question_match = re.match("[0-9]{1,3}[\.\)]{1,1}-{0,1} ", line)
            if question_match:
                current_question = question_match.group().replace(". ", "")
                current_question = current_question.replace(") ", "")
                current_question = current_question.replace(".- ", "")
                #print("Line -> " + current_question + " -> " + line)
                preguntas_parseo[current_question] = line
                question_mode = True
                answer_mode = False
                continue

            if re.match("[a-dA-D][\.\)] ", line):
                #print("Respuesta: current_question: " + current_question + " -> " + line)
                if current_question not in respuestas_parseo:
                    answer_list = []
                    answer_list.append(line)
                    respuestas_parseo[current_question] = answer_list
                else:
                    #print("elsito")
                    #print(respuestas_parseo[current_question])
                    respuestas_parseo[current_question].append(line)
                #print(respuestas_parseo[current_question])
                question_mode = False
                answer_mode = True
                continue
            if question_mode is True:
                #print("qmode -> " + line)
                preguntas_parseo[current_question] = preguntas_parseo[current_question] + line
                continue
            if answer_mode is True:
                #print("amode -> " + line)
                respuestas_parseo[current_question][len(respuestas_parseo[current_question])-1] = \
                    respuestas_parseo[current_question][len(respuestas_parseo[current_question])-1] + line
                continue

        else:
            # Parse solutions
            #print("Parsing solution")
            #print(line.split())
            soluciones_parseo[line.split()[0]] = line.split()[1]
            #print(soluciones)
    return preguntas_parseo, respuestas_parseo, soluciones_parseo


def correccion(preguntas, soluciones, respuestas_usuario):
    preguntas_fallidas = []
    nota = 0
    total_preguntas = len(preguntas)
    valor_pregunta = 10 / total_preguntas

    aciertos = 0
    fallos = 0
    no_contestadas = 0

    for clave, pregunta in preguntas.items():
        if respuestas_usuario[clave].lower() == "z":
            # Pregunta sin respuesta
            print(clave + " No Contestada")
            preguntas_fallidas.append(clave)
            no_contestadas = no_contestadas + 1
            continue
        if soluciones[clave].lower() == respuestas_usuario[clave].lower():
            print(clave + " Acierto")
            nota = nota + valor_pregunta
            aciertos = aciertos + 1
        else:
            print(clave + " Fallo " + respuestas_usuario[clave].lower() + " -> " + soluciones[clave].lower())
            nota = nota - (valor_pregunta/2)
            preguntas_fallidas.append(clave)
            fallos = fallos + 1

    print("")
    print("Aciertos: " + str(aciertos))
    print("No contestadas: " + str(no_contestadas))
    print("Fallos: " + str(fallos))
    print("")
    print("Tu nota es: " + str(nota))
    return preguntas_fallidas


def correccion_silenciosa(preguntas, soluciones, respuestas_usuario):
    aciertos = 0
    fallos = 0
    no_contestadas = 0

    for clave, pregunta in preguntas.items():
        if respuestas_usuario[clave].lower() == "z":
            # Pregunta sin respuesta
            no_contestadas = no_contestadas + 1
            continue
        if soluciones[clave].lower() == respuestas_usuario[clave].lower():
            aciertos = aciertos + 1
        else:
            fallos = fallos + 1

    return aciertos, fallos, no_contestadas

def grafica(preguntas, soluciones, respuestas_usuario, file):
    aciertos = 0
    fallos = 0
    no_contestadas = 0

    nota = 0
    total_preguntas = len(preguntas)
    valor_pregunta = 10 / total_preguntas

    try:
        for clave, pregunta in preguntas.items():
            if respuestas_usuario[clave].lower() == "z":
                # Pregunta sin respuesta
                no_contestadas = no_contestadas + 1
                print("z", end = '')
                continue
            if soluciones[clave].lower() == respuestas_usuario[clave].lower():
                aciertos = aciertos + 1
                nota = nota + valor_pregunta
                print("-", end = '')
            else:
                fallos = fallos + 1
                nota = nota - (valor_pregunta/2)
                print("x", end = '')
    except Exception as error:
        print(" Incompleto", end = '')
    #print(" " + file)
    print(" " + file + " OK: " + str(aciertos) + " FAIL: " + str(fallos) + " NoC: " + str(no_contestadas) + " Nota: " + str(nota))
    return aciertos, fallos, no_contestadas

def repaso(preguntas, respuestas, soluciones):
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


def repasar_fallos(preguntas, respuestas, soluciones, preguntas_fallidas):
    respuesta_usuario = str(input("¿quieres repasar los fallos? (y/n):").lower().strip())
    while not re.match("^[yn]+$", respuesta_usuario):
        respuesta_usuario = str(input("¿quieres repasar los fallos? (y/n):").lower().strip())

    if respuesta_usuario == "y":
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


def uno_a_uno(tema, test, preguntas, respuestas, soluciones, respuestas_usuario, attempt_id):
    # Empieza el test al usuario
    for clave, pregunta in preguntas.items():
        bold(pregunta)
        for respuesta in respuestas[clave]:
            print(respuesta)
        if clave in respuestas_usuario:
            # In this case have just loaded a file
            print("Respuesta ya registrada, pasamos a la siguiente")
            continue
        respuesta_usuario = str(input("Respuesta:").lower().strip())
        while not re.match("^[abcdez]{1,1}$", respuesta_usuario):
            respuesta_usuario = str(input("Respuesta:").lower().strip())
        respuestas_usuario[clave] = respuesta_usuario
        # Always save up to last question
        save_dict_to_file(respuestas_usuario, "saves/respuestas_tema"+tema+"test"+test+attempt_id+".txt")

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
    preguntas_fallidas = correccion(preguntas, soluciones, respuestas_usuario)
    return preguntas_fallidas


def examen(preguntas, respuestas, soluciones):
    respuestas_usuario = {}
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
    preguntas_fallidas = correccion(preguntas, soluciones, respuestas_usuario)
    return preguntas_fallidas


def comprobar_parseo(preguntas, respuestas, soluciones):
    # Empieza el test al usuario
    respuestas_usuario = {}
    for clave, pregunta in preguntas.items():
        bold(pregunta)
        for respuesta in respuestas[clave]:
            print(respuesta)
        respuestas_usuario[clave] = "a"
        print("\n\n\n")

    preguntas_fallidas = correccion(preguntas, soluciones, respuestas_usuario)
    print("Fin del test. Correccion:")
    print("Si llega esto aquí todo parece ok")
    return preguntas_fallidas


def validar_test(preguntas, soluciones):
    if len(preguntas) != len(soluciones):
        print("pero tiene " + str(len(soluciones)) + " soluciones, hay algo raro")
        respuesta_usuario = ""
        while not re.match("^[yn]+$", respuesta_usuario):
            respuesta_usuario = str(input("¿quieres hacer el test de todas formas? (y/n):").lower().strip())
        if respuesta_usuario == "n":
            exit(0)


def list_files(tema):
    script_dir = os.path.dirname(__file__) # <-- absolute dir the script is in
    rel_path = ruta_tests
    abs_file_path = os.path.join(script_dir, rel_path)

    for file in os.listdir(abs_file_path):
        if file.startswith("tema" + tema + "test"):
            preguntas_temp, respuestas_temp, soluciones_temp = parsear_fichero(file)
            print(file + " -> " + str(len(preguntas_temp)) + " preguntas. " + str(len(soluciones_temp)) + " soluciones")

def list_save_files(tema, test, preguntas, respuestas, soluciones):
    script_dir = os.path.dirname(__file__) # <-- absolute dir the script is in
    rel_path = ruta_saves
    abs_file_path = os.path.join(script_dir, rel_path)

    list_dir = os.listdir(abs_file_path)
    list_dir = [f.lower() for f in list_dir]
    sorted(list_dir)
    for file in list_dir:
        if file.startswith("respuestas_tema" + tema + "test" + test):
            respuestas_temp = {}
            respuestas_temp.update(load_dict_from_file("saves/"+file))
            grafica(preguntas, soluciones, respuestas_temp, file)

def principal():

    print("Heyyyyy")
    modo = input("¿Que modo quieres? (examen,repaso,one,load):")
    tema = input("¿Que tema deseas probar?:")

    list_files(tema)

    test = input("¿Que test del tema " + tema + "?:")
    fichero_test = "tema" + tema + "test" + test + ".txt"
    preguntas, respuestas, soluciones = parsear_fichero(fichero_test)

    attempt_id = "-" + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') 

    if modo == "load":
        list_save_files(tema, test, preguntas, respuestas, soluciones)
        attempt_id = input("¿Cual de los guardados quieres?:")
        if attempt_id != "":
            attempt_id = "-" + attempt_id


    print("\n\n\n")
    print("id guardado -> " + attempt_id)
    print("Este test tiene " + str(len(preguntas)) + " preguntas")
    validar_test(preguntas, soluciones)
    print("\n\n\n")

    respuestas_usuario = {}
    preguntas_fallidas = []
    fecha_inicio = datetime.datetime.now()
    if modo == "repaso":
        repaso(preguntas, respuestas, soluciones)
    elif modo == "check":
        preguntas_fallidas = comprobar_parseo(preguntas, respuestas, soluciones)
    elif modo == "one":
        preguntas_fallidas = uno_a_uno(tema, test, preguntas, respuestas, soluciones, respuestas_usuario, attempt_id)
    elif modo == "load":
        respuestas_usuario.update(load_dict_from_file("saves/respuestas_tema"+tema+"test"+test+attempt_id+".txt"))
        preguntas_fallidas = uno_a_uno(tema, test, preguntas, respuestas, soluciones, respuestas_usuario, attempt_id)
    else:
        preguntas_fallidas = examen(preguntas, respuestas, soluciones)
    fecha_fin = datetime.datetime.now()
    print("Fin del tema " + tema + " test " + test)
    list_save_files(tema, test, preguntas, respuestas, soluciones)
    log_test(fecha_inicio, fecha_fin, tema, test, modo, preguntas, soluciones, respuestas_usuario)
    repasar_fallos(preguntas, respuestas, soluciones, preguntas_fallidas)

    print("Salida del tema " + tema + " test " + test)


principal()

# Cosas que faltan:
# Examen fruticultura es imagen y faltan preguntas de 34 a 41
# Tema 28 Test Mezclados 1 no se puede parsear, es imagen.
# Tema 28 Ademas hay muchisimos mas tests dentro de las carpetas de la ley!!
# Tema 25 monton de tests en la carpeta de actualización al nuevo estatuto por partes
# Tema 24 EBEP test 312 preguntas. Al parsearlo se ve mal
# Ya se metieron!!! PERO FALTAN LOS 4 PDFS de la carpeta TESTS NUEVOS (mal parseados). TESTs extra del tema 20,21,22
# TESTs extra del tema 13 test ley transparencia canaria (no creo que valga la pena)
# Tema 1 Falta por meter Test extra titulo preliminar
