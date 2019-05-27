#!/usr/bin/env python3

import os

ruta_tests = "tests_ala/"

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.last_tag = ""
        self.print_question = False
        self.print_choice = False
        self.print_explanation = False
        self.question_number = 0
        self.choice_letter = "A"
        self.correct_answers = {}
        self.explanations = {}
        super().__init__()

    def list_attrs(self):
        for attr in attrs:
            print("..")
            for element in attr:
                print("-> " + element)

    def handle_starttag(self, tag, attrs):
        self.last_tag = tag
        if (tag == "h4"):
            #print("Encountered a start tag: " + tag + " with attrs ")
            question_attr = [("class","")]
            if (attrs == question_attr):
                print("\n\n")
                self.print_question = True
                self.choice_letter = "A"

        if (tag == "label"):
            #print("Encountered a start tag: " + tag + " with attrs ")
            answer_attr = [("class","form-option-label")]
            if (attrs == answer_attr):
                self.print_choice = True

        if (tag == "div"):
            answer_attr = [("class","form-option form-option-inline  correcta")]
            answer_attr_2 = [("class","explicacion hidden")]
            if (attrs == answer_attr):
                self.correct_answers[self.question_number] = self.choice_letter
            elif (attrs == answer_attr_2):
                self.print_explanation = True



    def handle_endtag(self, tag):
        # if (tag == "h4"):
        #    print("Encountered an end tag :", tag)
        self.last_tag = ""
        if (tag == "body"):
            print("\n\nSOLUCIONES")
            for k, v in self.correct_answers.items():
                print(k, v)
            #for k, v in self.explanations.items():
            #    print(k, v)

    def handle_data(self, data):
        if (self.print_question == True):
            self.question_number+=1
            print(str(self.question_number) + ". " + data)
            self.print_question = False
            return
            
        if (self.print_choice == True):
            print(str(self.choice_letter) + ") " + data)
            self.choice_letter = chr(ord(self.choice_letter) + 1)
            self.print_choice = False
            return

        if (self.print_explanation == True):
            self.explanations[self.question_number] = str(data)
            self.print_explanation = False

def parsear_fichero(fichero_test):
    script_dir = os.path.dirname(__file__) # <-- absolute dir the script is in
    rel_path = ruta_tests + fichero_test
    abs_file_path = os.path.join(script_dir, rel_path)

    # path = "tema11test3.txt"
    test_file_loaded = open(abs_file_path, 'r')

    preguntas_parseo = {}
    respuestas_parseo = {}
    soluciones_parseo = {}

    question_mode = False
    answer_mode = False
    current_question = ""
    solution_mode = False
    #for line in test_file_loaded.readlines():
    parser = MyHTMLParser()
    parser.feed(test_file_loaded.read())


def principal():
    print("Inicio principal")
    parsear_fichero("t1.html")



principal()
