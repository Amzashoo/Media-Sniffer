from SPARQLWrapper import SPARQLWrapper, JSON

# Defining the endpoint to which queries are being sent
sparql = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")
sparql.setReturnFormat(JSON)

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

class TrackInfo:
  def __init__(self, **keys):
    self.name = ''
    self.uri = ''
    self.artist = ''
    self.release = ''
    self.duration = ''
    if 'uri' in keys and 'name' in keys:
      self._init3(keys['uri'], keys['name'])
    elif 'uri' in keys:
      self._init1(keys['uri'])
    elif 'name' in keys:
      self._init2(keys['name'])

  def _init3(self, uri, name):
    self.uri = uri
    self.name = name
    self.tags = []

  def _init1(self, uri):
    self.uri = uri
    self.name = ''
    self.tags = []
    self.style = {'name':'', 'uri':''}

  def _init2(self, name):
    self.name = name
    self.uri = ''
    self.tags = []
    self.style = {'name':'', 'uri':''}

  def get_name(self):
    if(self.name == ''):
      self.ask_name()
    return self.name

  def get_uri(self):
    if(self.uri == ''):
      self.ask_uri()
    return self.uri
  
  def get_duration(self):
    if(self.duration == ''):
      self.ask_duration()
    return self.duration

  def get_artist(self):
    if(self.artist == ''):
      self.ask_artist()
    return self.artist

  def get_release(self):
    if(self.release == ''):
      self.ask_release()
    return self.release


  def ask_uri(self, number=1):
    query = """
      %s
      SELECT ?artist WHERE
      {
      ?artist rdf:type   mo:Track;
              rdfs:label "%s".
      } LIMIT %s"""%(prefix, self.name, number)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    if len(results) == 0:
      return
    self.uri = results[0]['artist']['value']

  def ask_name(self, number=1):
    query = """
      %s
      SELECT ?name WHERE
      {
      <%s> rdf:type   mo:Track;
           rdfs:label ?name.
      } LIMIT %s"""%(prefix, self.uri, number)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    if len(results) == 0:
      return
    self.name = results[0]['name']['value']

  def ask_artist(self, number=1):
    """Returns the artist corresponding to a URI."""
    predicates = """
    <%s> foaf:maker ?maker .
    ?maker rdfs:label ?artist .
    """%self.get_uri()
    # Building the query to send.
    query = """
    %s
    SELECT DISTINCT ?artist WHERE
    {
      %s
    } LIMIT %s
    """%(prefix,predicates,1)
    sparql.setQuery(query)
    # Sending the query.
    result = sparql.query().convert()['results']['bindings'][0]
    self.artist = result['artist']['value']

  def ask_release(self, number=1):
    """Returns the artist corresponding to a URI."""
    predicates = """
    ?release mo:track <%s>.
    ?release rdf:type mo:Record.
    """%self.get_uri()
    # Building the query to send.
    query = """
    %s
    SELECT DISTINCT ?release WHERE
    {
      %s
    } LIMIT %s
    """%(prefix,predicates,1)
    sparql.setQuery(query)
    # Sending the query.
    result = sparql.query().convert()['results']['bindings'][0]
    self.release = result['release']['value']


  def ask_duration(self, number=1):
    """Returns the artist corresponding to a URI."""
    predicates = """
    <%s> mo:length ?length .
    """%self.get_uri()
    # Building the query to send.
    query = """
    %s
    SELECT DISTINCT ?length WHERE
    {
      %s
    } LIMIT %s
    """%(prefix,predicates,1)
    sparql.setQuery(query)
    # Sending the query.
    result = sparql.query().convert()['results']['bindings'][0]
    self.duration = result['length']['value']

