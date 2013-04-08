import mutagen
import mutagen.mp3 as MP3
from audio_info import AudioData

def get_mp3_tags(infile):
  mp3file = MP3.MP3(infile)
  # Tries to get information from the metadata
  # Tries to read the track title
  title = ""
  artist = ""
  try:
    title = "%s" %mp3file["TIT2"]
  except:
    pass
  # Tries to read the track artist
  try:
    artist = "%s" %mp3file["TPE2"]
  except:
    pass
  audio = AudioData(title, artist)
  return audio

def get_ogg_tags():
  return
