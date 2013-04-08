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


def get_uris(track, artist="", release="", number=5):
  """Returns a list of URIs corresponding to the title and the artist given."""
  predicates = """
    ?track dc:title "%s".
    """%track
  if artist != "":
    predicates = """
    %s
    ?track foaf:maker ?maker .
    ?maker rdfs:label "%s".
    """ %(predicates, artist)
  if release != "":
    predicates = """
    %s
    ?track mo:track ?album .
    ?album dc:title "%s" .
    """ %(predicates,release)
  # Building the query to send.
  query = """
  %s
  SELECT DISTINCT ?track WHERE
  {
    %s
  } LIMIT %s
  """%(prefix,predicates,number)
  sparql.setQuery(query)
  # Sending the query.
  results = sparql.query().convert()['results']['bindings']
  uris = []
  for result in results:
    uris.append(result['track']['value'])
  return uris  

def get_artist(uri):
  """Returns the artist corresponding to a URI."""
  predicates = """
  <%s> foaf:maker ?maker .
  ?maker rdfs:label ?artist .
  """%uri
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
  return result['artist']['value']
  

def get_release(uri):
  return get_releases([uri])[0]

def get_releases(uris):
  """Returns a list of album names corresponding to the list of URIs given."""
  albums = []
  for uri in uris:
    query = """
      %s
      SELECT DISTINCT ?album
      WHERE {
        ?albumid mo:track <%s> .
        ?albumid dc:title ?album .
      } LIMIT %s"""%(prefix,uri, 10)
    obFichier = open('/tmp/uri_trace1','a')
    obFichier.write(uri)
    obFichier.write("\n")
    obFichier.close()

    obFichier = open('/tmp/query_trace','a')
    obFichier.write(query)
    obFichier.write("\n")
    obFichier.close()
    
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    try:
      albums.append(results[0]['album']['value'])
    except:
      pass
  return albums


class Tag:
  def __init__(self, name, uid):
    self.uid = uid
    self.name = name


