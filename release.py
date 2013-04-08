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
    Release = _release
  except:
    pass

  print web_pages.head(THIS)
  print web_pages.release_description(Release)
  print web_pages.foot()


index()


