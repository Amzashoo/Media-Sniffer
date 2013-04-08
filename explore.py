#!/usr/bin/python
#import tag_methods as tags
import sys, os, glob
import rdflib
import logging, mutagen
from audio_info import AudioData
from mutagen.mp3 import MP3
import musicbrainzngs as mbngs
"""from musicbrainz2.webservice"""

mbngs.set_useragent(app="Hamza-Chouhs-awesome-app",version="1337")

audio_extensions=[".mp3",".ogg",".flac",".wav"]

#path = sys.argv[1]

def explore(path, alist, dlist):
  for infile in glob.glob(os.path.join(path, '*')):
    if os.path.isdir(infile):
      dlist.append(infile)
#     explore(infile, alist, dlist)
    else:
      append_if_audio(alist, infile)
  return {'files':alist,'directories':dlist}

def append_if_audio(alist, infile):
  ext = str.lower(os.path.splitext(infile)[-1])
  
  if ext in audio_extensions:
    alist.append(infile)

def search_from_file(infile):
  tags = tags_from_file(infile)
  query = query_from_tags(tags)
  get_recording_by_query(query)


#explore(path,0, search_from_file)

def list_audio_files(path):
  return explore(path,[],[])
