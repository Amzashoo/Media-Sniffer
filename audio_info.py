from rdflib.Graph import Graph
from rdflib import Literal, BNode, Namespace
from rdflib import RDF
import mutagen
import mutagen.mp3 as MP3
import os
import musicbrainzngs as mbngs
import Levenshtein
from Levenshtein import ratio
import sparql_queries

mbngs.set_useragent(app="Hamza-Chouhs-awesome-app",version="1337")
MinSimilarityRatio = 0.6
MusicOntology = Namespace(":http://purl.org/ontology/mo/")
mburl = "http://musicbrainz.org/recording/"

class AudioData:
  def __init__(self, ttitle="", aartist="", aalbum=""):
    self.title = ttitle
    self.artist = aartist
    self.album = aalbum

  def set_title(self, ttitle):
    """Sets the value for the TITLE field."""
    self.title = ttitle

  def set_artist(self, aartist):
    """Sets the value for the ARTIST field."""
    self.artist = aartist
  
  def set_album(self, aalbum):
    """Sets the value for the ALBUM field."""

  def tags_from_file(self, infile): # A optimiser...
    """Sets the information for the current object to that contained in the
       file which path has been sent as an argument."""
    switch = {'.mp3':get_mp3_tags,
              '.ogg':get_ogg_tags}
    extension = str.lower(os.path.splitext(infile)[-1])
    new = switch.get(extension, nomatch)(infile)
    self.title = new.title
    self.artist = new.artist
#   self.album = new['album']

def nomatch(foo):
  vide = {'artist':'', 'title':''}
  return vide

# Ajouter la possibilite de choisir l'album. Mais alternative a abandonner.
def query_from_tags(tags):
  """Returns a "good" query from the tags given.
     If no information is provided by the tags, returns an empty string."""
  if tags["artist"] != "":
    return "%s,artist:%s" %(tags["title"], tags["artist"])
  elif (tags["title"] != ""):
    return "%s" %tags["title"]
  else:
    return ""

  
def get_mp3_tags(infile):
  """Retrieves information about a file from its MP3 tags."""
  mp3file = MP3.MP3(infile)
  # Tries to get information from the metadata
  # Tries to read the track title
  title = ""
  artist = ""
  album = ""
  try:
    title = "%s" %mp3file["TIT2"]
  except:
    pass
  # Tries to read the track artist
  try:
    artist = "%s" %mp3file["TPE2"]
  except:
    pass
  # Tries to read the album name
  try:
    album = "%s" %mp3file["TALB"]
  except:
    pass
  audio = AudioData(title, artist, album)
  return audio

def get_ogg_tags():
  return

class FileInfo:
  """Represents an audio file : contains its name, its metadata and the inform-
    -ation got by the query."""
  def __init__(self, path):
    self.filepath = path[3:]
    self.uri = ''
    self.releases = None
    self.localData = AudioData()
    self.remoteData = AudioData()
    # Reads metadata from file.
    self.localData.tags_from_file(path)
    # Doesn't try to get data from nothing !
    self.uri = 42
    if(self.localData.title != ""):
      try:
        self.uris = sparql_queries.get_uris(self.localData.title,
                                           self.localData.artist,
                                           self.localData.album)
        self.uri = self.uris[0]
      except:
        try:
          self.uris = sparql_queries.get_uris(self.localData.title,
                                          self.localData.artist)
          self.uri = self.uris[0]
        except:
          pass
      # If we do not know the artist and the Sparql query gave nothing...
#      if(self.uri == 42):  
#        remoteResults = self.get_remote_data()
#        self.computeData(remoteResults

  def get_releases(self):
    if(self.releases == None):
      self.releases = sparql_queries.get_releases(self.uris)
    return self.releases

  def computeData(self, results):
    """Choses the record/artist couple with the best correspondancy."""
    records = results['recording-list']
    score_list = []
    # Adding every record which title have a high enough similarity ratio.
    for record in records:
      title_r = ratio(record['title'], self.localData.title)
      if title_r >= MinSimilarityRatio:
        score_list.append({'title_r':title_r,'record':record,'artist_r':0,'artist':''})
    # Finding the best artist correspondance for each record.
    best_artist=''
    best_ratio = 0
    best_element = {'title_r':0, 'record':records[0], 'artist_r':0, 'artist':self.localData.artist}
    # Doesn't try to compare artists if no one has been given.
    if(self.localData.artist != ""):
      for element in score_list:
        best_local_name = ''
        best_local_ratio = 0
        for artist_credit in element['record']['artist-credit']:
          local_name = artist_credit['artist']['name']
          local_ratio = ratio(artist, self.localData.artist)
          # Locally maximizing the ratio for each artist corresponding to the record.
          if local_ratio > best_local_ratio:
            best_local_name = local_name
            best_local_ratio = local_ratio
          # We are trying to maximise the best ratio.
          if local_ratio > best_ratio:
            best_element = element
            best_ratio = local_ratio
            element['artist'] = best_local_name
            element['artist_r'] = local_ratio
      if best_ratio > MinSimilarityRatio:
        record = best_element
        self.remoteData.title = record['record']['title']
        self.remoteData.artist = record['artist']
      else:
        self.remoteData.artist = ''
        self.remoteData.title = ''
    else:
      self.remoteData.title = score_list[0]['record']['title']
      self.remoteData.artist = score_list[0]['record']['artist-credit'][0]['artist']['name']

  def get_remote_data(self):
    """Sends a query corresponding to the title/artist of the track to the
       MusicBrainz server. Careful : each query can take a few seconds."""
    query = ""
    # No query if not data was found.
    if self.localData.title == "":
      return
    # Adding details to the query.
    query += self.localData.title
    if self.localData.artist != "":
      query += ",artist:%s" %self.localData.artist
    # Sending it.
    results = mbngs.search_recordings(query, limit=10)
    return results   
    

    #self.remoteData.title = results['recording-list'][0]['title']
    #self.remoteData.artist = results['recording-list'][0]['artist-credit'][0]['artist']['name']
    
    #print "Track found :", results['recording-list'][0]['title'], "by", results['recording-list'][0]['artist-credit'][0]['artist']['name']
      

