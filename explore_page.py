import sys
sys.path.append("./www/test")
import explore
import web_pages


def index():
  path = "./"
  for arg in THIS.args:
    path = "%s/%s"%(path, arg) 
  index = "index%s"%THIS.ext
  result = explore.list_audio_files(path)
  audio_files = result['files']
#  print audio_files
  directories = result['directories']
  print web_pages.head(THIS)
  print """<div id="uparrow"> %s audio files found.</div>"""%len(audio_files)
  pair = True
  print web_pages.dir_element("../", pair, THIS)
  for directory in directories:
    pair = not pair
    print web_pages.dir_element(directory, pair, THIS)
  for file in audio_files:
    pair = not pair
    print web_pages.audio_element(file, pair, THIS)
  print """<div id="downarrow"> Hamza Chouh, 2012 </div>"""
  print web_pages.foot()


index()
