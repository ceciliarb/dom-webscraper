from parser import parseFiles
import subprocess
import os
import time

# Python program to print
# duplicates from a list
# of integers
def Repeat(x):
    _size = len(x)
    repeated = []
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i] == x[j] and x[i] not in repeated:
                repeated.append(x[i])
    return repeated
 
def countEdicoes():
  edicoes_dir = f"{os.curdir}/edicoes"
  input_dir = f"{os.curdir}/input"

  lote1 = os.listdir(f"{edicoes_dir}/lote1")
  lote1 = [x for x in lote1 if not x.startswith('_')]
  lote1Cnt = len(lote1)
  lote2 = os.listdir(f"{edicoes_dir}/lote2")
  lote2 = [x for x in lote2 if not x.startswith('_')]
  lote2Cnt = len(lote2)
  lote3 = os.listdir(f"{edicoes_dir}/lote3")
  lote3 = [x for x in lote3 if not x.startswith('_')]
  lote3Cnt = len(lote3)
  lote4 = os.listdir(f"{edicoes_dir}/lote4")
  lote4 = [x for x in lote4 if not x.startswith('_')]
  lote4Cnt = len(lote4)
  probs = os.listdir(f"{input_dir}/problemas")
  probs = [x for x in probs if not x.startswith('_')]
  probCnt = len(probs)
  probs2 = os.listdir(f"{input_dir}/problemas2")
  probs2 = [x for x in probs2 if not x.startswith('_')]
  prob2Cnt = len(probs2)

  edicoesTratadas = lote1 + lote2 + lote3 + lote4 + probs + probs2
  edicoesTratadas = list(map(removeExtension, edicoesTratadas))
  edicoesTratadasCnt = len(edicoesTratadas)
  edicoesTratadasDuplicadas = Repeat(edicoesTratadas)
  edicoesTratadasCntDuplicadas = len(edicoesTratadasDuplicadas)

  with open(f"{input_dir}/code/edicoes.txt", 'r') as f:
    edicoesATratar = set(f.read().splitlines())
    totalEdicoes = len(edicoesATratar)

  print(f"lote1: \t\t{lote1Cnt}")
  print(f"lote2: \t\t{lote2Cnt}")
  print(f"lote3: \t\t{lote3Cnt}")
  print(f"lote4: \t\t{lote4Cnt}")
  print(f"problemas: \t{probCnt}")
  print(f"problemas2: \t{prob2Cnt}")
  print(f"soma: \t\t{ edicoesTratadasCnt }")
  print(f"duplicadas: \t{ edicoesTratadasCntDuplicadas }")
  print(f"total: \t\t{totalEdicoes}")
  print(f"----------------------------------------------------------")
  with open(f"{os.curdir}/tratadas.txt", "w") as edTratadas:
    edTratadas.write("\n".join(sorted(edicoesTratadas)))
  with open(f"{os.curdir}/tratadas_duplicadas.txt", "w") as edTratadas:
    edTratadas.write("\n".join(sorted(edicoesTratadasDuplicadas)))
  with open(f"{os.curdir}/tratadas_lote1.txt", "w") as edTratadas:
    edTratadas.write("\n".join(sorted(map(removeExtension, lote1))))
  with open(f"{os.curdir}/tratadas_lote2.txt", "w") as edTratadas:
    edTratadas.write("\n".join(sorted(map(removeExtension, lote2))))
  with open(f"{os.curdir}/tratadas_lote3.txt", "w") as edTratadas:
    edTratadas.write("\n".join(sorted(map(removeExtension, lote3))))
  with open(f"{os.curdir}/tratadas_lote4.txt", "w") as edTratadas:
    edTratadas.write("\n".join(sorted(map(removeExtension, lote4))))
  with open(f"{os.curdir}/tratar.txt", "w") as edTratar:
    edTratar.write("\n".join(sorted(edicoesATratar)))


def removeExtension(filename):
  return filename[:-4]

if __name__ == "__main__":
    import sys
    countEdicoes()
