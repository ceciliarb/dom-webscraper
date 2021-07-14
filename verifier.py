from parser import parseFiles
import subprocess
import os
import time

def verifyAtos(num_edicao):
  base = f"{os.curdir}/output/{num_edicao}"
  htmls = f"{base}/htmls"
  pdfs_com_anexos = f"{base}/pdfs-com-anexos"
  pdfs_sem_anexos = f"{base}/pdfs-sem-anexos"

  if os.path.exists(base):
    htmls_cnt = len(os.listdir(htmls))
    pdfs_sem_anexos_cnt = len(os.listdir(pdfs_sem_anexos))
    if os.path.exists(pdfs_com_anexos):
      pdfs_com_anexos_cnt = len(os.listdir(pdfs_com_anexos))
      pdfs_sem_anexos_cnt -= pdfs_com_anexos_cnt
    else:
      pdfs_com_anexos_cnt = 0

    if htmls_cnt != (pdfs_com_anexos_cnt + pdfs_sem_anexos_cnt):
      print(f"{num_edicao}:\tNOK\thtmls: {htmls_cnt} | com {pdfs_com_anexos_cnt} | sem {pdfs_sem_anexos_cnt}")
    else:
      print(f"{num_edicao}:\tOK\thtmls: {htmls_cnt} | com {pdfs_com_anexos_cnt} | sem {pdfs_sem_anexos_cnt}")
  else:
    print(f"{num_edicao}:\tNot verified")
 
def verifyAnexos(num_edicao):
  base = f"{os.curdir}/files/{num_edicao}"

  if os.path.exists(base):
    for ato in sorted(os.listdir(base)):
      ato_dir = f"{base}/{ato}"
      if os.path.isdir(ato_dir):
        pdfs = f"{ato_dir}/pdfs"
        to_convert = f"{ato_dir}/to-convert"
        pdfs_cnt = 0
        if os.path.exists(pdfs):
          pdfs_cnt = len(os.listdir(pdfs))
        to_convert_cnt = 0
        if os.path.exists(to_convert):
          to_convert_cnt = len(os.listdir(to_convert))

        if pdfs_cnt != (to_convert_cnt):
          print(f"{num_edicao}:\tNOK\tpdfs: {pdfs_cnt} != to-convert {to_convert_cnt} | ato {ato}")
        else:
          print(f"{num_edicao}:\tOK\tpdfs: {pdfs_cnt} == to-convert {to_convert_cnt} | ato {ato}")
        
        if pdfs_cnt > 0 :
          for anx_file in os.listdir(to_convert):
            if os.path.getsize(f"{to_convert}/{anx_file}") == 0:
              print(f"\t{num_edicao}:\tNOK\tpdf VAZIO | ato {ato}")
  else:
    print(f"{num_edicao}:\tNot verified")

if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    check_ato = '--atos' in sys.argv
    check_anx = '--anexos' in sys.argv

    if os.path.isdir(path):
      input_dir = path
      if input_dir[-1] != "/": 
        input_dir = input_dir+"/"

      dir_files = sorted(os.listdir(input_dir))
      for filename in dir_files:
        if filename.endswith(".txt") and not filename.startswith("_"): 
          if check_ato: verifyAtos(filename[:-4])
          if check_anx: verifyAnexos(filename[:-4])

    else:
      if path.endswith(".txt"): 
        if check_ato: verifyAtos(filename[:-4])
        if check_anx: verifyAnexos(filename[:-4])
