import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
from song import Song
from tkinter import *
from tkinter import ttk
from collections import deque

stack = deque()
start_time = time.time()

cid = 'f604655815fc4c69b4888d600e2823d3'
sid = '7960cf00874949e4a044526506edd06a'
redirect_url = 'http://localhost:9000'
scope = 'user-modify-playback-state user-read-currently-playing user-read-playback-state'

auth_manager = SpotifyOAuth(client_id = cid, client_secret = sid, redirect_uri = redirect_url, scope = scope)
spotify_obj = spotipy.Spotify(auth_manager = auth_manager)

def get_playlist_tracks(playlist_id):
    results = spotify_obj.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = spotify_obj.next(results)
        tracks.extend(results['items'])
    return tracks

def parse_playlist(playlist_id):
	results = get_playlist_tracks(playlist_id)
	count = 0
	start = time.time()
	track_list = []

	for item in results:
		count = count + 1
		track = item['track']
		song_obj = Song(track['uri'], spotify_obj)
		track_list.append(song_obj)

	delta = time.time() - start
	print("%d tracks analyzed in %.2f seconds" % (count, delta,))
	print(track_list)
	return track_list

def queue_list(tracks):
	for track in tracks:
		spotify_obj.add_to_queue(track.song_id)
		time.sleep(0.2)

def skip_track(): #WORKING
	track = Song(spotify_obj.currently_playing()['item']['uri'], spotify_obj)
	spotify_obj.seek_track(track.duration)

def parse_load_tracks(*args):
	uri = playlist_id_entry.get()
	if uri == "":
		return
	print("Starting parse...")
	track_list = parse_playlist(uri)
	track_list.sort(key = lambda x: x.tempo) #sort list by tempo
	print(track_list)
	for x in track_list:
		stack.append(x)
	queue_list(track_list)



root = Tk()
root.title("djpitviper")

mainframe = ttk.Frame(root, padding="100 100 100 100")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

playlist_id = StringVar()
playlist_id_entry = ttk.Entry(mainframe, width=100)
playlist_id_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Button(mainframe, text="Load Playlist", command=parse_load_tracks).grid(column=2, row=2, sticky=W)
ttk.Button(mainframe, text="Skip Track", command=skip_track).grid(column=2, row=3, sticky=W)

#ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

playlist_id_entry.focus()
root.bind("<Return>", parse_load_tracks)

root.mainloop()
"""
while True:
	#print(stack)
	root.update_idletasks()
	root.update()
	if len(stack) > 0:
		#time.sleep(60.0 - ((time.time() - start_time) % 60.0))
		print(stack)
		temp = Song(spotify_obj.currently_playing()['item']['uri'], spotify_obj)
		if temp.time_left() <= 12050.0:
			spotify_obj.add_to_queue(stack.pop().song_id)

			#spotify_obj.add_to_queue(stack.pop().song_id)
"""

#print(json.dumps(spotify_obj.current_playback(), indent=4))

#TODO: 
# 1. use a Stack to make a custom queue that loads from the top down
# 	 by finding a way to add a new song to the internal Spotify queue when a song is changing/ending
#	 we can find track progress, add a way to get that quickly and subtract it from duration
#
# 2. use a socket or webserver to open a server on a local network, then use that to create a new gui that can be used on mobile
#
# 3. build a track list out of clusters of song instead of just song by song, then randomize the order inside the clusters. Ideally
#	 results in a more random feel that still has the same transition quality
#
# 4. add Soundcloud integration (pause currently playing/fade between Soundcloud and Spotify) once Soundcloud
#	 enables new developer applications