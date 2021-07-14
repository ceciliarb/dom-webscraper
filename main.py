from parser import parseFiles
import subprocess
import os
import time

def convertFile(input_file_path, start_time, clear, move, out_dir):
  with open(input_file_path, 'r') as input_file:
    lines = input_file.read().splitlines()
  num_edicao = input_file_path.split('/')[-1].split('.')[0]
  print("============================ Edicao: %s ==================================================" % num_edicao)
  parseFiles(lines, num_edicao, start_time, clear, move, out_dir)

if __name__ == "__main__":
    import sys
    clear = '--no-clear' not in sys.argv
    move  = '--no-move' not in sys.argv
    clock = '--no-clock' not in sys.argv
    path  = sys.argv[1]
    out_dir = 'edicoes/'
    if len(sys.argv) >= 3:
      out_dir  = sys.argv[2]

    if clock:
      print(":::::::::::::::::::::::::::::::::::::")
      start_time = time.time()
      print(time.asctime(time.localtime(start_time)))

    if os.path.isdir(path):
      input_dir = path
      if input_dir[-1] != "/": 
        input_dir = input_dir+"/"

      dir_files = sorted(os.listdir(input_dir))
      for filename in dir_files:
        if filename.endswith(".txt") and not filename.startswith("_"): 
          convertFile(input_dir+filename, start_time, clear, move, out_dir)

    else:
      if path.endswith(".txt"): 
        convertFile(path, start_time, clear, move, out_dir)
