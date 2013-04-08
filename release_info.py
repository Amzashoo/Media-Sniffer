from SPARQLWrapper import SPARQLWrapper, JSON

# Usual prefixes for MusicBrainz queries
prefix = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
PREFIX rel: <http://purl.org/vocab/relationship/>
PREFIX lingvoj: <http://www.lingvoj.org/ontology#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX tags: <http://www.holygoat.co.uk/owl/redwood/0.1/tags/>
PREFIX db: <http://dbtune.org/musicbrainz/resource/>
PREFIX geo: <http://www.geonames.org/ontology#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX bio: <http://purl.org/vocab/bio/0.1/>
PREFIX mo: <http://purl.org/ontology/mo/>
PREFIX vocab: <http://dbtune.org/musicbrainz/resource/vocab/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mbz: <http://purl.org/ontology/mbz#>"""


# Defining the endpoint to which queries are being sent
sparql = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")
sparql.setReturnFormat(JSON)



class ReleaseInfo:
  """A class representing a musical release."""
  def __init__(self, **keys):
    """Constructor."""
    self.name = ''
    self.uri = ''
    self.artist = None
    self.tracks = []
    self.cover = ""
    if 'uri' in keys and 'name' in keys:
      self._init3(keys['uri'], keys['name'])
    elif 'uri' in keys:
      self._init1(keys['uri'])
    elif 'name' in keys:
      self._init2(keys['name'])

  def _init3(self, uri, name):
    """Sub-constructor."""
    self.uri = uri
    self.name = name

  def _init1(self, uri):
    """Sub-constructor."""
    self.uri = uri
    self.name = ''

  def _init2(self, name):
    """Sub-constructor."""
    self.name = name
    self.uri = ''

  def get_artist(self):
    """Returns the artist who made the release."""
    if self.artist == None:
      self.ask_artist()
    return self.artist

  def get_tracks(self):
    """Returns a list of the tracks of the release."""
    if self.tracks == []:
      self.ask_tracks()
    return self.tracks

  def get_cover(self):
    """Returns a URL to the releases's cover."""
    if self.cover == "":
      self.ask_cover()
    return self.cover

  def get_uri(self):
    """Returns the URI of the release."""
    if self.uri == '':
      self.ask_uri()
    return self.uri

  def get_name(self):
    """Returns the name of the release."""
    if self.name == '':
      self.ask_name()
    return self.name

  def ask_name(self, limit=10):
    """Asks the release name to the MB server."""
    query = """
      %s
      SELECT ?name WHERE
      {
      <%s> rdfs:label ?name.
      } LIMIT %s"""%(prefix, self.uri, limit)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    if len(results) == 0:
      return
    self.name = results[0]['name']['value']

  def ask_uri(self, limit=10):
    """Asks the release URI to the MB server. You need to have specified the name to use this."""
    if self.name == "":
      return
    query = """
      %s
      SELECT ?release WHERE
      {
      ?release dc:title "%s".
      ?release rdf:type mo:Record. 
      } LIMIT %s"""%(prefix, self.name, limit)
    sparql.setQuery(query)
    print query
    results = sparql.query().convert()['results']['bindings']
    if len(results) == 0:
      return
    self.uri = results[0]['release']['value']
  
  def ask_cover(self, limit=1):
    """Asks the release cover URL to the MB server."""
    tags = []
    query = """
      %s
      SELECT ?cover WHERE
      {
        <%s> vocab:albummeta_coverarturl ?cover .
      } LIMIT %s"""%(prefix, self.get_uri(), limit)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    self.cover = results[0]['cover']['value']


  def ask_artist(self, limit=1):
    """Asks the artist to the MB server."""
    tags = []
    query = """
      %s
      SELECT ?artist WHERE
      {
        <%s> foaf:maker ?artist .
      } LIMIT %s"""%(prefix, self.get_uri(), limit)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    self.artist = results[0]['artist']['value']



  def ask_tracks(self, number=100):
    """Asks the tracks list to the MB server."""
    records = []
    query = """
      %s
      SELECT ?track ?name WHERE
      {
        <%s> mo:track ?track.
        ?track dc:title ?name.
      } LIMIT %s"""%(prefix, self.get_uri(), number)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    for result in results:
      records.append(result['track']['value'])
    self.tracks = records

