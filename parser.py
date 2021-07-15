#############################################
# requisitos:                               #
# - sudo apt install libreoffice            #
# - sudo apt install ghostscript            #
# - sudo apt install wkhtmltopdf            #
# - sudo apt install unzip                  #
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
import traceback
from bs4 import BeautifulSoup, Comment, Tag

def find_comment_sibling(soup, inner_text):
  tag = soup.find(text=lambda text:isinstance(text, Comment) and inner_text in text )
  if tag:
    return [tag.next.next]
  else:
    return []

def monthStringToNumber(month):
  return {
    "Janeiro": 1,
    "January": 1,
    "Fevereiro": 2,
    "February": 2,
    "Março": 3,
    "March": 3,
    "Abril": 4,
    "April": 4,
    "Maio": 5,
    "May": 5,
    "Junho": 6,
    "June": 6,
    "Julho": 7,
    "July": 7,
    "Agosto": 8,
    "August": 8,
    "Setembro": 9,
    "September": 9,
    "Outubro": 10,
    "October": 10,
    "Novembro": 11,
    "November": 11,
    "Dezembro": 12,
    "December": 12
    }.get(month, 0)

def preProcess(id, num_edicao):
  url = "http://portal6.pbh.gov.br/dom/iniciaEdicao.do?method=DetalheArtigo&pk=" + str(id)
  resp = requests.get(url)
  content = resp.text
  # remove tags especificas do windows
  clean_content = content.replace("<![if !supportEmptyParas]>", "").replace("<![endif]>", "").replace("<o:p>", "").replace("</o:p>", "")
  # corrige valor de width
  #  clean_content = clean_content.replace("980px", "88%")

  # alterando cabecalho (grayscale)
  cabecalho_local = "http://localhost:8000/assets/Logo-dom-Belo-Horizonte_grayscale.jpg"
  clean_content = clean_content.replace("../imagens/Logo-dom-Belo-Horizonte.jpg", cabecalho_local)
  soup = BeautifulSoup(clean_content, 'html5lib')
  # remove tags de layout
  # cabecalho
  #  tags = soup.find_all(href=re.compile("iniciaEdicao"))
  tags = []
  tags = tags + (soup.find_all("td", id="direita"))
  tags = tags + find_comment_sibling(soup, "fim materia")
  tags = tags + soup.select("script")
  for tag in tags:
    tag.extract()
  # removendo links hidden
  for a in soup.find_all(name="a"):
    if len(a.contents) == 0:
      a.extract()
  
  css = Tag(soup, name='style')
#  css.append("table, img, blockquote, p, span, h1, div {page-break-inside: avoid; !important }")
#  css.append("* {     page-break-inside: avoid; page-break-before: avoid; page-break-after: avoid;   }")
  soup.head.append(css)
  clean_content = soup.prettify()

  # removendo comentarios
  clean_content = re.sub(r'<!--.*?-->', "", clean_content)

  # extrai link de arquivo de download
  exts  = '(?:zip|doc|docx|rtf|xls|xlt|pdf|ps|gif|jpg|jpeg|tif|tiff|ZIP|DOC|DOCX|RTF|XLS|XLT|PDF|PS|GIF|JPG|JPEG|TIF|TIFF)'
  regex = r'(<a .{0,50}?href\=[\'|\"]\/dom.{0,50}?\/Files\/.*?\.'+exts+'[\'|\"].{0,50}?>.*?<\/a>)'
  
  links_download = re.findall(regex, clean_content, flags=re.S)
  links_name = []
  for link in links_download:
    if link:
      link = re.search(r'(href\=[\'|\"]\/dom.{0,50}?Files\/.*?\.'+exts+'[\'|\"])', link, flags=re.S).group(0)
      link = link.replace("href='", "").replace("'", "").replace('href="', '').replace('"', '')

      # removendo o link de download
      clean_content = clean_content.replace(link, "#")
      print('Salvando arquivo: '+link)
      try:
        arquivos = saveFile(id, num_edicao, link)
        links_name = links_name + arquivos
      
      except RuntimeError as e:
        links_name.append('__FALHA__')


  arr = soup.select("div.datahoje")[0].string.split(" ")
  data = f"{arr[1]}/{monthStringToNumber(arr[3])}/{arr[5]}"

  curr_dir = os.getcwd()
  html_dir_out = curr_dir + '/output/'+str(num_edicao)+'/htmls'
  if not os.path.exists(html_dir_out):
    os.makedirs(html_dir_out)
  with open(html_dir_out + '/' + str(id) + ".html", "w") as text_file:
    text_file.write(soup.prettify())

  return (links_name, data)

def saveFile(id, num_edicao, url):
  
  try:
#    extension = url.split('.')[-1]
#    resp = requests.get("http://portal6.pbh.gov.br" + url, stream=True)
#    
#    if resp.status_code == 200:
#      # salvar arquivo
#      curr_dir = os.getcwd()
#      directory = curr_dir + '/files/' + str(num_edicao) + '/' + str(id) + '/to-convert'
#      if not os.path.exists(directory):
#        os.makedirs(directory)
#      path = url.split('/')[-1]
#  
#      with open(directory+'/'+path, "wb") as f:
#        if extension not in ['gif', 'jpeg', 'jpg', 'png', 'tiff', 'tif']:
#          f.write(resp.content)
#        else:
#          resp.raw.decode_content = True
#          shutil.copyfileobj(resp.raw, f)
  
#      if os.path.getsize(f"{directory}/{path}") == 0:
#        raise RuntimeError
  
#    else:
#      raise RuntimeError

    arquivos = []
    curr_dir = os.getcwd()
    directory = curr_dir + '/files/' + str(num_edicao) + '/' + str(id) + '/to-convert'
    arquivo = url.split('/')[-1]
    if not os.path.exists(directory):
      os.makedirs(directory)
    subprocess.run(["wget", f"http://portal6.pbh.gov.br{url}", "-O", f"{directory}/{arquivo}"])

    if os.path.getsize(f"{directory}/{arquivo}") == 0:
      raise RuntimeError
    else: 
      if arquivo.split('.')[1].lower() == 'zip':
        subprocess.run(["unzip", "-j", f"{directory}/{arquivo}", "-d", directory])
        arqs = os.listdir(directory)
        for arq in arqs:
          if arq.split('.')[1].lower != 'zip':
            arquivos.append(arq.split('.')[0])
          else:
            os.remove(f"{directory}/{arquivo}")
      else:
        arquivos.append(arquivo.split('.')[0])

  except:
    print('Falha ao baixar arquivo "%s"' % url)
    raise RuntimeError

  return arquivos

def convertToPDF(file_path, output_path, wk=False, num_edic="", data="1/1/1111"):
  if not os.path.exists(output_path):
    os.makedirs(output_path)
  ext = (file_path.split('/')[-1]).split('.')[-1]
  if ext == 'pdf':
    subprocess.run(["cp", file_path, output_path])
  else:
    if wk:
      file_name = ".".join((file_path.split('/')[-1]).split('.')[0:-1])
      texto_rodape = f"Esta é uma reprodução digitalizada do conteúdo presente no DOM nº {num_edic}, de {data}.\nhttps://dom-web.pbh.gov.br"
      print("WkHtmlToPdf %s --> %s" % (file_path, output_path + file_name + ".pdf"))
      subprocess.run(["wkhtmltopdf", "-q", "-B", "20", "--footer-spacing", "10", "--footer-font-size", "8", "--footer-center", texto_rodape, file_path, output_path + file_name + ".pdf"])
    else:
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

def convertAtoToPDF(id, num_edicao, data):
  curr_dir   = os.getcwd()
  input_dir  = curr_dir + '/output/' + str(num_edicao) + '/htmls/' + str(id) + '.html'
  output_dir = curr_dir + '/output/' + str(num_edicao) + '/pdfs-sem-anexos/'
  convertToPDF(input_dir, output_dir, True, num_edicao, data)

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

def clear(num_edicao):
  curr_dir = os.getcwd()
  try:
    for filename in os.listdir(curr_dir):
      if filename.endswith(".html") or filename.endswith(".pdf"): 
        os.remove(filename)
    if os.path.exists(f"{curr_dir}/files/{num_edicao}"):
      shutil.rmtree(f'{curr_dir}/files/{num_edicao}')
      print(f'limpando files {curr_dir}/files/{num_edicao}')
    if os.path.exists(f"{curr_dir}/output/{num_edicao}"):
      print(f'limpando output {curr_dir}/output/{num_edicao}')
      shutil.rmtree(f'{curr_dir}/output/{num_edicao}')
  except OSError as e:
    print("Error: %s" % e.strerror)

def markAs(num_edic, id, tipo):
  input_dir = os.curdir+"/input/"
  if not os.path.exists(input_dir+"done/"):
    os.makedirs(input_dir+"done/")
  if os.path.exists(input_dir+num_edic+".txt"):
    os.rename(input_dir+num_edic+".txt", input_dir+"done/"+num_edic+".txt")
  with open(os.curdir+'/logs/'+tipo+'_' + str(id) + ".txt", "a") as text_file:
    text_file.write(str(num_edic)+"\n")

def markAsDone(path, id):
  markAs(path, id, 'migradas')

def markAsProblem(path, id):
  markAs(path, id, 'problemas')

def markAsDoneBefore(path, id):
  markAs(path, id, 'migradas_anteriormente')

def parseFiles(ids, num_edicao=0, start_time=0, bClear=True, bMove=True, output_dir="edicoes/"):
  try:
 #   if(bClear): 
 #     clear(num_edicao)
    out_dir  = "output/"+str(num_edicao)+"/"
    edi_file = out_dir+str(num_edicao)+".pdf"
    edi_dir  = output_dir
    subprocess.run(["mkdir", "-p", out_dir, edi_dir])
    paths = []
    for id in ids:
      bMoved = False

      if os.path.exists(edi_file):
        print("Edicao ja existe! Pegando proxima edicao")
        if bMove: markAsDoneBefore(num_edicao, str(start_time))
        bMoved = True
        continue

      else:
        id = int(id)
        print('---------------------------- ATO: %s ----------------------------------------' % str(id))
        try:
          links, data = preProcess(id, num_edicao)
#          convertAllAnexosToPDF(id, num_edicao)
          convertAtoToPDF(id, num_edicao, data)

          print(links)
          for link in links:
            print("Inserindo ao pdf root: "+link)
            if link != '__FALHA__':
              insertPDFAnexoToPDFAto(id, num_edicao, link)

          if links:
            if '__FALHA__' in links:
              if bMove: 
                markAsProblem(num_edicao, str(start_time))
                bMoved = True
              if len(set(links)) == 1:
                paths.append(out_dir+"pdfs-sem-anexos/"+str(id)+".pdf")
              else:
                paths.append(out_dir+"pdfs-com-anexos/"+str(id)+".pdf")
            else:
              paths.append(out_dir+"pdfs-com-anexos/"+str(id)+".pdf")
          else:
            paths.append(out_dir+"pdfs-sem-anexos/"+str(id)+".pdf")

        except RuntimeError as e:
          print("Erro! Pegando proxima edicao")
          if bMove: 
            markAsProblem(num_edicao, str(start_time))
            bMoved = True
          continue

    subprocess.run(["gs", "-dBATCH", "-dNOPAUSE", "-q", "-sDEVICE=pdfwrite", "-sOutputFile="+edi_dir+str(num_edicao)+".pdf", *paths])
    if bMove and not bMoved: 
      markAsDone(num_edicao, str(start_time))
      bMoved = True
    
  except Exception:
    print("Erro ao gerar edicao %s" % num_edicao)
    print("Erro %s" % traceback.print_exc())
    if bMove and not bMoved: 
      markAsProblem(num_edicao, str(start_time))

if __name__ == "__main__":
    import sys
    ids = sys.argv[1:]
    parseFiles(ids)

