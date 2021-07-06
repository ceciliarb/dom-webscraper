#############################################
# requisitos:                               #
# - sudo apt install libreoffice            #
# - sudo apt install ghostscript            #
# -  pip install requests                   #
# -  pip install beautifulsoup4             #
# -  pip install html5lib                   #
#############################################
import re
import os
import io
import shutil
import requests
import subprocess
from bs4 import BeautifulSoup, Comment

def find_comment_sibling(soup, inner_text):
  tag = soup.find(text=lambda text:isinstance(text, Comment) and inner_text in text )
  if tag:
    return [tag.next.next]
  else:
    return []


def preProcess(id, num_edicao):
  url = "http://portal6.pbh.gov.br/dom/iniciaEdicao.do?method=DetalheArtigo&pk=" + str(id)
  resp = requests.get(url)
  content = resp.text
  # remove tags especificas do windows
  clean_content = content.replace("<![if !supportEmptyParas]>", "").replace("<![endif]>", "").replace("<o:p>", "").replace("</o:p>", "")
  # corrige valor de width
  clean_content = clean_content.replace("980px", "88%")

  # extrai link de arquivo de download
  exts  = '(?:\.doc|\.rtf|\.xls|\.pdf|\.gif)'
  regex = r'(<a .{0,50} href\=[\'|\"]\/dom\/.{0,50}Files.*?'+exts+'[\'|\"].{0,20}>.*?<\/a>)'
  links_download = re.findall(regex, clean_content, flags=re.S)
  links_name = []
  for link in links_download:
    if link:
      link = re.search(r'(href\=[\'|\"]\/dom\/.{0,50}Files.*?'+exts+'[\'|\"])', link, flags=re.S).group(0)
      link = link.replace("href='", "").replace("'", "").replace('href="', '').replace('"', '')
      path = (link.split('/')[-1]).split('.')[0]
      ext = (link.split('/')[-1]).split('.')[1]
      links_name.append(path)
      # removendo o link de download
      clean_content = clean_content.replace(link, "#")
      print('Salvando arquivo: '+link)
      saveFile(id, num_edicao, link)

  soup = BeautifulSoup(clean_content, 'html5lib')
  # remove tags de layout
  tags = soup.find_all(href=re.compile("iniciaEdicao"))
  tags = tags + (soup.find_all("td", id="direita"))
  tags = tags + find_comment_sibling(soup, "fim materia")
  tags = tags + soup.select("script")
  for tag in tags:
    tag.extract()

  curr_dir = os.getcwd()
  html_dir_out = curr_dir + '/output/'+str(num_edicao)+'/htmls'
  if not os.path.exists(html_dir_out):
    os.makedirs(html_dir_out)
  with open(html_dir_out + '/' + str(id) + ".html", "w") as text_file:
    text_file.write(soup.prettify())

  return links_name

def saveFile(id, num_edicao, url):
  extension = url.split('.')[-1]
  resp = requests.get("http://portal6.pbh.gov.br" + url, stream=True)

  if resp.status_code == 200:
    # salvar arquivo
    curr_dir = os.getcwd()
    directory = curr_dir + '/files/' + str(num_edicao) + '/' + str(id) + '/to-convert'
    if not os.path.exists(directory):
      os.makedirs(directory)
    path = url.split('/')[-1]

    with open(directory+'/'+path, "wb") as file:
      if extension not in ['gif', 'jpeg', 'jpg', 'png']:
        file.write(resp.content)
      else:
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, file)
  else:
    print('Falha ao baixar arquivo "%s"' % url)
    exit()

  return path.split('.')[0]

def convertToPDF(file_path, output_path):
  subprocess.run(["lowriter", "--headless", "--convert-to", "pdf", "--outdir", output_path, file_path])

def convertAllAnexosToPDF(id, num_edicao):
  curr_dir = os.getcwd()
  output_dir = curr_dir + '/files/' + str(num_edicao) + '/' + str(id) + '/pdfs'
  input_dir = curr_dir + '/files/' + str(num_edicao) + '/' + str(id) + '/to-convert'

  if not os.path.exists(input_dir):
    os.makedirs(input_dir)
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  for filename in os.listdir(input_dir):
    print('Convertendo arquivo: '+filename)
    convertToPDF(input_dir+'/'+filename, output_dir)

def convertAtoToPDF(id, num_edicao):
  curr_dir   = os.getcwd()
  input_dir  = curr_dir + '/output/' + str(num_edicao) + '/htmls/' + str(id) + '.html'
  output_dir = curr_dir + '/output/' + str(num_edicao) + '/pdfs-sem-anexos/'
  convertToPDF(input_dir, output_dir)

def mergePDF(pdf_path_1, pdf_path_2, out_path):
  # resolvendo o problema do ghostscript nao aceitar um output igual a um dos inputs
  if pdf_path_1 == out_path or pdf_path_2 == out_path:
    out_path_old = out_path
    out_path     = out_path.replace(".pdf", "___out___.pdf")

  subprocess.run(["gs", "-dBATCH", "-dNOPAUSE", "-q", "-sDEVICE=pdfwrite", "-sOutputFile="+out_path, pdf_path_1, pdf_path_2])
  
  if "___out___" in out_path:
    os.remove(out_path_old)
    os.rename(out_path, out_path.replace("___out___", ""))

def insertPDFAnexoToPDFAto(id, num_edicao, nome_arquivo):
  curr_dir = os.getcwd()
  anx_file = curr_dir + '/files/'+str(num_edicao)+'/'+str(id)+'/pdfs/'+nome_arquivo+".pdf"
  ato_file = curr_dir + '/output/'+str(num_edicao)+'/pdfs-com-anexos/'+str(id)+'.pdf'
  if not os.path.exists(ato_file):
    ato_file = curr_dir + '/output/'+str(num_edicao)+'/pdfs-sem-anexos/'+str(id)+'.pdf'
  
  out_dir  = curr_dir + '/output/'+str(num_edicao)+'/pdfs-com-anexos/'
  print("Mesclando: '%s' com '%s'" % (ato_file, anx_file))
  if not os.path.exists(out_dir):
    os.makedirs(out_dir)
  out_file = out_dir+str(id)+".pdf"
  mergePDF(ato_file, anx_file, out_file)

def insertPDFAtoToPDFEdicao(id, num_edicao):
  curr_dir = os.getcwd()
  ato_file = curr_dir + '/output/'+str(num_edicao)+'/pdfs-com-anexos/'+str(id)+'.pdf'
  tmp_file = curr_dir + '/output/'+str(num_edicao)+"/"+str(num_edicao)+"_temp.pdf"
  edi_file = curr_dir + '/output/'+str(num_edicao)+"/"+str(num_edicao)+".pdf"


  print("Mesclando: '%s' com '%s'" % (tmp_file, ato_file))
  mergePDF(tmp_file, ato_file, edi_file)

def clear():
  curr_dir = os.getcwd()
  try:
    for filename in os.listdir(curr_dir):
      if filename.endswith(".html") or filename.endswith(".pdf"): 
        os.remove(filename)
    if os.path.exists(curr_dir + "/files"):
      shutil.rmtree(curr_dir + '/files')
    if os.path.exists(curr_dir + "/output"):
      shutil.rmtree(curr_dir + '/output')
  except OSError as e:
    print("Error: %s" % e.strerror)

def parseFiles(ids, num_edicao=0, bClear=True):
  try:
    if(bClear): 
      clear()
    out_dir  = "output/"+str(num_edicao)+"/"
    edi_file = out_dir+str(num_edicao)+".pdf"
    edi_dir  = "edicoes/"
    subprocess.run(["mkdir", "-p", out_dir, edi_dir])
    paths = []
    for id in ids:
      id = int(id)
      print('---------------------------- ID: %s ----------------------------------------' % str(id))
      links = preProcess(id, num_edicao)
      convertAllAnexosToPDF(id, num_edicao)
      convertAtoToPDF(id, num_edicao)
      for link in links:
        print("Inserindo ao pdf root: "+link)
        insertPDFAnexoToPDFAto(id, num_edicao, link)

      if links:
        paths.append(out_dir+"pdfs-com-anexos/"+str(id)+".pdf")
      else:
        paths.append(out_dir+"pdfs-sem-anexos/"+str(id)+".pdf")

    subprocess.run(["gs", "-dBATCH", "-dNOPAUSE", "-q", "-sDEVICE=pdfwrite", "-sOutputFile="+edi_dir+str(num_edicao)+".pdf", *paths])

  except Exception as e:
    print("Erro ao gerar edicao %s" % num_edicao)
    print("Erro %s" % e)

if __name__ == "__main__":
    import sys
    ids = sys.argv[1:]
    parseFiles(ids)

