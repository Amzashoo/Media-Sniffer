import random
from sparql_queries import Tag
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

class ArtistInfo:
  def __init__(self, **keys):
    self.name = ''
    self.uri = ''
    self.tags = []
    self.members = []
    self.records = []
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

  def ask_uri(self, number=1):
    query = """
      %s
      SELECT ?artist WHERE
      {
      ?artist rdf:type   mo:MusicArtist;
              rdfs:label "%s".
      } LIMIT %s"""%(prefix, self.name, number)
    print query
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    if len(results) == 0:
      return
    print results
    self.uri = results[0]['artist']['value']

  def ask_name(self, number=1):
    query = """
      %s
      SELECT ?name WHERE
      {
      <%s> rdf:type   mo:MusicArtist;
           rdfs:label ?name.
      } LIMIT %s"""%(prefix, self.uri, number)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    if len(results) == 0:
      return
    self.name = results[0]['name']['value']
  def get_tags(self):
    if self.tags == []:
      self.ask_tags()
    return self.tags

  def get_records(self):
    if self.records == []:
      self.ask_records()
    return self.records

  def get_members(self):
    if self.members == []:
      self.ask_members()
    return self.members

  def ask_tags(self, limit=10):
    tags = []
    query = """
      %s
      SELECT ?tag ?name WHERE
      {
        <%s> tags:taggedWithTag ?tag.
        ?tag rdfs:label ?name .
      } LIMIT %s"""%(prefix, self.get_uri(), limit)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    for result in results:
      tags.append(Tag(result['name']['value'], result['tag']['value']))
    print results
    self.tags = tags

  def ask_records(self, limit=100):
    records = []
    query = """
      %s
      SELECT ?member ?name WHERE
      {
        <%s> foaf:member ?member.
        ?member rdfs:label ?name.
      } LIMIT %s"""%(prefix, self.get_uri(), limit)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    for result in results:
      members.append(ArtistInfo(uri = result['member']['value'], name = result['name']['value']))
    self.records = records

  def ask_members(self, limit=10):
    members = []
    query = """
      %s
      SELECT ?member ?name WHERE
      {
        <%s> foaf:member ?member.
        ?member rdfs:label ?name.
      } LIMIT %s"""%(prefix, self.get_uri(), limit)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    for result in results:
      members.append(ArtistInfo(uri = result['member']['value'], name = result['name']['value']))
    self.members = members

  def same_tagged_artists(self, limit=10):
    artists = []
    query = """
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
PREFIX mbz: <http://purl.org/ontology/mbz#>
      SELECT ?artist WHERE
      {
     
       <%s> tags:taggedWithTag ?tag.
       ?artist tags:taggedWithTag ?tag.
       ?artist rdf:type mo:MusicArtist.
      } LIMIT %s OFFSET %s
"""%(self.get_uri(), limit, 0)
    sparql.setQuery(query)
    results = sparql.query().convert()['results']['bindings']
    for result in results:
      artists.append(ArtistInfo(uri = result['artist']['value']))
    return artists
