from parser import parseFiles
import time

def convertFile(input_file_path, clear):
  print(input_file_path)
  with open(input_file_path, 'r') as input_file:
    lines = input_file.read().splitlines()
  num_edicao = input_file_path.split('/')[-1].split('.')[0]
  parseFiles(lines, num_edicao, clear)

def markAsDone(path):
  input_dir = '/'.join(path.split('/')[0:-1])
  filename  = path.split('/')[-1]
  os.rename(path, input_dir+"/done/"+filename)
  

if __name__ == "__main__":
    import sys
    import os
    clear = '--no-clear' not in sys.argv
    move  = '--no-move' not in sys.argv
    clock = '--no-clock' not in sys.argv
    path  = sys.argv[1]

    try:
      if clock:
        print(":::::::::::::::::::::::::::::::::::::")
        print(time.asctime(time.localtime(time.time())))

      if os.path.isdir(path):
        input_dir = path
        if input_dir[-1] != "/": 
          input_dir = input_dir+"/"
        for filename in os.listdir(input_dir):
          if filename.endswith(".txt") and not filename.startswith("_"): 
            convertFile(input_dir+filename, clear)
            if move: markAsDone(input_dir+filename)
      else:
        if path.endswith(".txt"): 
          convertFile(path, clear)
          if move: markAsDone(path)
    except Exception as e:
      print("Erro! %s" % e)
