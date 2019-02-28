#!/usr/bin/env python3

import subprocess
from subprocess import run
import os
#import yaml

class _bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def bold(textToPrint):
    print(_bcolors.BOLD + textToPrint + _bcolors.ENDC)

def log(textToPrint):
    print(_bcolors.OKBLUE + textToPrint + _bcolors.ENDC)

def warning(textToPrint):
    print(_bcolors.WARNING + textToPrint + _bcolors.ENDC)

def error(textToPrint):
    print(_bcolors.FAIL + textToPrint + _bcolors.ENDC)

"""
def loadYaml(file):
  result = {}
  try:
    f = open(file, 'r')
    result = yaml.load(f)
    f.close()

  except Exception:
    print ("ERROR: cannot read file '" + file + "'")
    exit (1)

  return result
"""
def save_dict_to_file(dic, file_name):
    f = open(file_name,'w')
    f.write(str(dic))
    f.close()

def load_dict_from_file(file_name):
    f = open(file_name,'r')
    data=f.read()
    f.close()
    return eval(data)

def save_list_to_file(list, file_name):
    with open(file_name, 'w') as filehandle:
        for listitem in list:
            filehandle.write('%s\n' % listitem)

def load_list_to_file(file_name):
    # define an empty list
    list = []

    # open file and read the content in a list
    with open(file_name, 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            current_place = line[:-1]

            # add item to the list
            list.append(current_place)

    return list

def acceptCommitInGerrit(short_hash, gerrit_port, gerrit_url):
    # Accept commit using ssh protocol. User should be valid in gerrit and also ssh key exchange configured
    # ssh -p 29418 gerrit.ericsson.se gerrit review --verified +1 --code-review +2 --submit --project SAPC/esapc 1dc8030
    run(['ssh', '-p', gerrit_port, gerrit_url, 'gerrit', 'review', '--verified', '+1',
         '--code-review', '+2', '--submit', '--project', 'SAPC/esapc', short_hash], check=True)

def acceptCurrentCommitInGerrit(gerrit_port, gerrit_url):
    # Get the current hash using git rev-parse --short HEAD
    git_response = run(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, encoding='utf-8', check=True)
    commit_hash = git_response.stdout.rstrip()
    log("Current Commit: " + commit_hash)
    acceptCommitInGerrit(commit_hash, gerrit_port, gerrit_url)

def askUser(user_question):
    # Or if not input("Are you sure? (y/n): ").lower().strip()[:1] == "y": exit(1)
    check = str(input(user_question + " (y/n): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return askUser(user_question)

def getCurrentSAPCRevisionAndRelease():
    # Project root:
    project_root = subprocess.Popen("git rev-parse --show-toplevel", stdout=subprocess.PIPE, encoding='utf-8',
                                    shell=True).stdout.read().strip()
    if not project_root: exit(1)
    # Path to build yaml file:
    build_yaml_file = os.path.join(project_root, 'software', 'build.yaml')

    build_yaml = loadYaml(build_yaml_file)
    product_revision = build_yaml["product"]["version"]
    product_release = build_yaml["product"]["id"].split("_")[1]

    return product_revision, product_release

def getCurrentRepoPath():
    project_root = subprocess.Popen("git rev-parse --show-toplevel", stdout=subprocess.PIPE, encoding='utf-8',
                                    shell=True).stdout.read().strip()
    if not project_root: exit(1)
    return project_root

# Alphabetical increase
def getNextRevision(st):
  next_str = ""
  increment = '0'*(len(st)-1) + '1'
  index = len(st) -1
  carry = 0
  curr_digit = 0
  while(index>=0):
    if (st[index].isalpha()):
      curr_digit = (ord(st[index]) + int(increment[index]) + carry)
      if curr_digit > ord('z'):
        curr_digit -= ord('a')
        curr_digit %= 26
        curr_digit += ord('a')
        carry = 1
      else:
        carry = 0
      curr_digit = chr(curr_digit)
      next_str += curr_digit

    elif (st[index].isdigit()):
      curr_digit = int(st[index]) + int(increment[index]) + carry
      if curr_digit > 9:
        curr_digit %= 10
        carry = 1
      else:
        carry = 0
      next_str += str(curr_digit)
    index -= 1

  return next_str[::-1]
