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

def parse(path, out_dir, lote_file="", parseEdicoes=False, parseAtos=True):
  arr = []
  edicoes = []
  with open(path, "r") as text_file:
    previous_num_edicao = ''
    for line in text_file.readlines():
      num_edicao, tipo_edicao, id_ato, ordem = line.split(';')
      if tipo_edicao != "P": 
          num_edicao = num_edicao+"_"+tipo_edicao
      else:  
          num_edicao = num_edicao

#      print("num edicao: %s   |  num edicao anterior: %s" % (num_edicao, previous_num_edicao))

      edicoes_lote = []
      if lote_file != "": 
        with open(f"{os.curdir}/{lote_file}", "r") as lote:
          edicoes_lote = lote.read().splitlines()

      if parseAtos:
        # condicao de saida do loop (nova edicao)
        if previous_num_edicao != '' and previous_num_edicao != num_edicao:         
          if (len(edicoes_lote) > 0 and previous_num_edicao in edicoes_lote) or len(edicoes_lote) == 0:
            if parseEdicoes:
              edicoes.append(previous_num_edicao)

            with open(f"{os.curdir}/{out_dir}/{previous_num_edicao}.txt", "w") as output:
              output.write('\n'.join(arr))
            print(arr)
            arr = []

      # pega atos apenas das edicoes listadas
      if (len(edicoes_lote) > 0 and previous_num_edicao in edicoes_lote) or len(edicoes_lote) == 0:
        arr.append(id_ato)
      previous_num_edicao = num_edicao

  if parseEdicoes:
      with open(f"{os.curdir}/{out_dir}/__edicoes.txt", "w") as output:
        output.write('\n'.join(sorted(set(edicoes))))


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    out_dir = sys.argv[2]
    lote_file = sys.argv[3]
    bEdicoes = '--edicoes' in sys.argv
    bAtos = '--atos' in sys.argv

    if not os.path.exists(out_dir):
      os.makedirs(out_dir)
    else:
      shutil.rmtree(out_dir)
      os.makedirs(out_dir)

    parse(path, out_dir, "", bEdicoes, bAtos)
    
    
    
    
    
    
    
    
