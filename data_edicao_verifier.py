from parser import parseFiles
import os
from bs4 import BeautifulSoup

def verifyEdicao(num_edicao):
  htmls = f"{os.curdir}/output/{num_edicao}/htmls"
  
  for html in sorted(os.listdir(htmls)):
    htmlContent = ""
    with open(f"{htmls}/{html}", "r") as arq:
      htmlContent = arq.read()

    soup = BeautifulSoup(htmlContent, 'html5lib')
    edicao = soup.select("div.edicao")[0].string.strip().split(" ")[-1]
    if edicao == num_edicao:
      print(f"{num_edicao}:\tOK")
    else:
      print(f"{num_edicao}:\tNOK\thtml edicao: {edicao} != edicao {num_edicao}")

if __name__ == "__main__":
    import sys
    path = sys.argv[1]

    if os.path.isdir(path):
      input_dir = path
      if input_dir[-1] != "/": 
        input_dir = input_dir+"/"

      dir_files = sorted(os.listdir(input_dir))
      for filename in dir_files:
        if filename.endswith(".txt") and not filename.startswith("_"): 
          verifyEdicao(filename[:-4])

    else:
      if path.endswith(".txt"): 
        verifyEdicao(sys.argv[1][:-4])
