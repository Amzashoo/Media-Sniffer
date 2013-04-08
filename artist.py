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
    Artist = _artist
  except:
    pass

  print web_pages.head(THIS)
  print web_pages.artist_description(name = Artist)
  print web_pages.foot()


index()


