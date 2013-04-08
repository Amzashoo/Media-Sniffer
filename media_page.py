import sys
sys.path.append("./www/test")
import explore
import web_pages
import audio_info
import sparql_queries

def index():
  path = "./"
  file = ""
  try:
    file = _file
  except:
    pass

  print web_pages.head(THIS)
  audio = audio_info.FileInfo(file)
#  print audio.uri
  print web_pages.song_description(file)
  print web_pages.foot()


index()
