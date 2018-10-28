import os
import sys
import glob
import json
import time
import pickle
from pprint import pprint

import spotipy
from spotipy.util import prompt_for_user_token
from lyricfetch import Song


def chunker(seq, size):
    """
    Utility function to iterate over a list in chunks.
    """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


# Check requirements
if not os.path.isfile('config.json'):
    print('Please create a config.json using the template')
    sys.exit(1)

if len(sys.argv) < 2:
    print('Usage: {0} username'.format(sys.argv[0]))
    sys.exit(1)

with open('config.json') as f:
    config = json.load(f)

# Get our authentication going
username = sys.argv[1]
scope = 'user-library-read, user-library-modify'
token = prompt_for_user_token(
    username, scope, client_id=config['client_id'],
    client_secret=config['client_secret'],
    redirect_uri=config['redirect_uri'])

if not token:
    print("Can't get token for", username)
    sys.exit(1)
sp = spotipy.Spotify(auth=token)


# Get the list of albums in the spotify library
curr_albums = dict()
page = 50
offset = 0
while True:
    query = sp.current_user_saved_albums(limit=page, offset=offset)
    for item in query['items']:
        item = item['album']
        name = item['name']
        artist = item['artists'][0]['name']
        url = item['external_urls']['spotify']
        curr_albums[(artist, name)] = url
    if len(query['items']) < page:
        break
    offset += page

# Get the local list of albums
if os.path.isfile('.cache-musiclib'):
    with open('.cache-musiclib', 'rb') as f:
        songs = pickle.load(f)
else:
    music_home = os.path.expanduser('~/Music')
    mp3files = glob.iglob(music_home + '/**/*.mp3', recursive=True)
    songs = set(Song.from_filename(f) for f in mp3files)
    with open('.cache-musiclib', 'wb') as f:
        pickle.dump(songs, f)
library = set((song.artist, song.album) for song in songs)

# Load the cached album url list
if os.path.isfile('.cache-album_urls'):
    with open('.cache-album_urls', 'rb') as f:
        album_urls = pickle.load(f)
else:
    album_urls = dict()

# Get the urls for all the albums we don't already have
for artist, album in library:
    if (artist, album) in album_urls:
        continue
    query = sp.search(q=f'{artist} - {album}', type='album')
    try:
        url = query['albums']['items'][0]['external_urls']['spotify']
        album_urls[(artist, album)] = url
    except Exception:
        print("Could not get url for", album)

# Save the cached urls
with open('.cache-album_urls', 'wb') as f:
    pickle.dump(album_urls, f)

# Use the urls to filter out albums we already have
curr_urls = set(curr_albums.values())
album_urls = {a: u for a, u in album_urls.items() if u not in curr_urls}
pprint(album_urls)

# Actually add the new albums to our remote collection
for chunk in chunker(list(album_urls.values()), 20):
    sp.current_user_saved_albums_add(chunk)
    time.sleep(2)
