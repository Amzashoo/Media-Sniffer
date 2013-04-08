import audio_info
import sparql_queries
from artist_info import ArtistInfo
from track_info import TrackInfo
from release_info import ReleaseInfo

HOME = "/test"

def content(elements):
  pair = True
  for element in elements:
    if pair:
      print """<div class="item">"""
    else:
      print """<div class="itemA"/>"""
    print """<img src="%s"/>"""%element['image']
    print "%s --- %s"%(element['artist'],element['title'])
    print "</div>"

def head(THIS):
  return """
<!DOCTYPE html>
<html>
<head>
  <meta charest="UTF-8">
  <meta http-equiv="Content-Type" CONTENT="text/html;charset=utf-8">
  <link rel="stylesheet" type="text/css" href="%s">
  <title>Media Sniffer</title>
  <script src="%s"></script>
  <script>
     audiojs.events.ready(function() {
      var as = audiojs.createAll();
    });
  </script>
</head>
<body>
  <div id="menuBar">
    <table id="menu">
      <tr class="button">
      <td class="button"><a href="explore_page.py">Explore</a></td>
      <td class="button"><a href="about.htm">About</a></td>
      </tr>
    </table>
  </div>
  <div id="content">
    <div id="contentBody">
"""%(THIS.rel("design.css"),THIS.rel('audiojs/audio.min.js'))

def foot():
  return """
    </div>
  </div>
</body>
"""

def audio_element(name, pair, THIS):
  image = "images/note.png"
  str = ""
  if pair:
    str+= """<div class="item">"""
  else:
    str+= """<div class="itemA">"""
  str+= """<img src="%s"/>"""%THIS.rel(image)
  filename = name.split('/')[-1]
  filenameREL = THIS.rel(filename)
  page = "%s/media_page.py?file=%s"%(HOME,name)
  str+= """<span class="item-text"><a href="%s">%s</a></span>"""%(page,filename)
  str+= "</div>"
  return str


def dir_element(name, pair, THIS):
  image = "images/dir.png"

  str = ""
  if pair:
      str+= """<div class="item">"""
  else:
    str+= """<div class="itemA">"""
  str+= """<img src="%s"/>"""%THIS.rel(image)
  ## Resoudre PB url INDEX
  if name != "../":
    filename = name.split('/')[-1]
    newurl = "%s/%s"%(THIS.url,filename)
  else:
    filename = name
    newurl = THIS.url
    newurl = newurl[:-1]
    while newurl[-1] != '/':
      newurl = newurl[:-1]
    newurl = newurl[:-1]

  str+= """<span class="item-text"><a href="%s">%s</a></span>"""%(newurl,filename)
  str+= "</div>"
  return str


def song_description(name):
  str = ""
  pathu = ""
  audio = audio_info.FileInfo(name)
  pathsss = audio.filepath.split('/')[1:]
  for el in pathsss:
    pathu = "%s/%s"%(pathu,el)
  title = audio.localData.title
  artist = sparql_queries.get_artist(audio.uri)
  track = TrackInfo(name = title)
  release = ReleaseInfo(uri = track.get_release())
  release = release.get_name()
  str += """<table border="10" id="titletab"><tr id="row1">"""
  str += """<td rowspan="2" id="imagetd"> <img src="images/audio-volume-high.png"/> </td>"""
  str += """<td id="song_td"><div id="song_title">%s</div></td></tr>"""%title
  str += """<tr id="row2"><td id="song_artist"><div id="song_artist">in <a href="release.py?release=%s">%s</a> by <a href="artist.py?artist=%s">%s</a></div></td></tr>"""%(release, release,artist,artist)
#  str += """<tr id="row3"><td class="section">Releases</td><td class="element"></td></tr>"""
#  pair = False
#  for release in releases:
#    link = "release.py?release=%s"%release.get_name()
#    pair = not pair
#    if pair:
#      str += """<tr id="row_even"><td class="section"></td><td class="element"><a href="%s">%s</a></td></tr>"""%(link,release.get_name())
#    else: 
#      str += """<tr id="row_odd"><td class="section"></td><td class="element"><a href="%s">%s</a></td></tr>"""%(link,release.get_name())
  str += """<tr><td id="foot_cell"></td> <td class="element"><audio src="%s" preload="auto" /></td></tr>"""%(pathu)#audio.path
  str += """</table>"""
  return str


def release_description(Name):
  str = ""
  release = ReleaseInfo(name = Name)

  name = release.get_name()
  artist = ArtistInfo(uri = release.get_artist())
  tracks = release.get_tracks()
  cover = release.get_cover()
   
  str += """<table border="10" id="titletab"><tr id="row1">"""
  str += """<td rowspan="2" id="imagetd"> <img src="%s"/> </td>"""%(cover)
  str += """<td id="song_td"><div id="song_title">%s</div></td></tr>"""%name
  str += """<tr id="row2"><td id="song_artist"><div id="song_artist">by <a href="artist.py?artist=%s">%s</a></div></td></tr>"""%(artist.get_name(),artist.get_name())
  str += """<tr id="row3"><td class="section">Tracks</td><td class="element"></td></tr>"""
  pair = False
  for track in tracks:
    pair = not pair
    if pair:
      str += """<tr id="row_even"><td class="section"></td><td class="element">%s</td></tr>"""%(TrackInfo(uri=track).get_name())
    else: 
      str += """<tr id="row_odd"><td class="section"></td><td class="element">%s</td></tr>"""%(TrackInfo(uri=track).get_name())
  str += """</table>"""
  return str



def artist_description(**keys):
  str = ""
  artist = ArtistInfo(**keys)
  name = artist.get_name()
  uri = artist.get_uri()
  tags = artist.get_tags()
  members = artist.get_members()
    
  str += """<table border="10" id="titletab"><tr id="row1">"""
  str += """<td rowspan="2" id="imagetd"> <img src="images/audio-volume-high.png"/> </td>"""
  str += """<td id="song_td"><div id="song_title">%s</div></td></tr>"""%name
  str += """<tr id="row2"><td id="song_artist"><div id="song_artist">"""
  if len(members) > 0:
    for nm in members[:-1]:
      str += """<a href="artist_info.py?artist=%s">%s</a>, """%(nm.get_name(),nm.get_name())
    nm = members[-1]
    str += """<a href="artist_info.py?artist=%s">%s</a>"""%(nm.get_name(),nm.get_name())
  else:
    str += "</br>"
  str += """</div></td></tr>"""
  #Adding tags
  if len(tags) > 0:
    str += """<tr id="row3"><td class="section">Tags</td><td class="element"></td></tr>"""
    str += """<tr id="row_even"><td class="section"></td><td class="element">"""
    for tag in tags[:-1]:
      str += """%s, """%tag.name
    str += """%s."""%tags[-1].name
  #Adding similar artists
  
  sartists = artist.same_tagged_artists()
  if len(sartists) > 0:
    str += """<tr id="row3"><td class="section">Similar artists</td><td class="element"></td></tr>"""
  pair = False
  for sartist in sartists:
    pair = not pair
    link = "artist.py?artist=%s"%sartist.get_name()
    if pair:
      str += """<tr id="row_even"><td class="section"></td><td class="element"><a href="%s">%s</a></td></tr>"""%(link,sartist.get_name())
    else:
      str += """<tr id="row_odd"><td class="section"></td><td class="element"><a href="%s">%s</a></td></tr>"""%(link,sartist.get_name())
  str += """</td></tr><tr><td id="foot_cell"></td> <td class="element"></td></tr>"""
  str += """</table>"""
  return str

#  str += """<tr id="row3"><td class="section">Releases</td><td class="element"></td></tr>"""
#  pair = False
#  for release in releases:
#    link = "release.py?release=%s"%release.get_name()
#    pair = not pair
#    if pair:
#      str += """<tr id="row_even"><td class="section"></td><td class="element"><a href="%s">%s</a></td></tr>"""%(link,release.get_name())
#    else: 
#      str += """<tr id="row_odd"><td class="section"></td><td class="element"><a href="%s">%s</a></td></tr>"""%(link,release.get_name())









