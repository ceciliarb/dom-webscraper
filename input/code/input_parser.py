#############################################
# requisitos:                               #
# - sudo apt install libreoffice            #
# - sudo apt install ghostscript            #
# -  pip install beautifulsoup4             #
#############################################
import re
import os
import shutil
import requests
import subprocess
from bs4 import BeautifulSoup, Comment

def parse(path):
  arr = []
  with open(path, "r") as text_file:
    previous_num_edicao = ''
    for line in text_file.readlines():
      num_edicao, tipo_edicao, id_ato, ordem = line.split(';')
      if tipo_edicao != "P": 
          num_edicao = num_edicao+"_"+tipo_edicao
      else:  
          num_edicao = num_edicao

      print("num edicao: %s   |  num edicao anterior: %s" % (num_edicao, previous_num_edicao))

      if previous_num_edicao != '' and previous_num_edicao != num_edicao:
        with open(previous_num_edicao+".txt", "w") as output:
          output.write('\n'.join(arr))
        print(arr)
        arr = []

      arr.append(id_ato)
      previous_num_edicao = num_edicao


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    parse(path)
    
    
    
    
    
    
    
    
