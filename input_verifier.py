from parser import parseFiles
import os

def verifyInput(num_edicao):
  inputOriginal = f"{os.curdir}/input/code/out/{num_edicao}.txt"
  with open(inputOriginal, 'r') as input:
    iO = sorted(input.read().splitlines())

  if os.path.exists(inputOriginal):
    inputExecutadoL1 = f"{os.curdir}/input/lote1/{num_edicao}.txt"
    inputExecutadoL2 = f"{os.curdir}/input/lote2/{num_edicao}.txt"
    inputExecutadoL3 = f"{os.curdir}/input/lote3/{num_edicao}.txt"
    inputExecutadoL4 = f"{os.curdir}/input/lote4/{num_edicao}.txt"
    inputExecutadoP1 = f"{os.curdir}/input/problemas/{num_edicao}.txt"
    inputExecutadoP2 = f"{os.curdir}/input/problemas2/{num_edicao}.txt"
    inputs = [inputExecutadoL1, inputExecutadoL2, inputExecutadoL3, inputExecutadoL4, inputExecutadoP1, inputExecutadoP2]

    iE = []
    for inputExecutado in inputs:
      if os.path.exists(inputExecutado):
        with open(inputExecutado, 'r') as input:
          iE = sorted(input.read().splitlines())
        break

    if iE == iO:
      print(f"{num_edicao}:\tOK")
    else:
      print(f"{num_edicao}:\tNOK\tcount executado: {len(iE)} != count original {len(iO)}")
      print(f"\t\texecutado: {iE}")
      print(f"\t\toriginal: {iO}")
      
  else:
    print(f"{num_edicao}:\tNot verified")

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
          verifyInput(filename[:-4])

    else:
      if path.endswith(".txt"): 
        verifyInput(sys.argv[1][:-4])
