import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
from song import Song
from collections import deque
from tkinter import *
from tkinter import ttk
import random
import sys

stack = deque()

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
		song_obj = Song(track, spotify_obj)
		track_list.append(song_obj)

	delta = time.time() - start
	print("%d tracks analyzed in %.2f seconds" % (count, delta,))
	return track_list

def queue_list(tracks):
	bucket = [0]
	bucket.pop(0)
	while(len(tracks) > 0):
		while len(bucket) <= 5:
			if len(tracks) > 0:
				bucket.append(tracks.pop(0)) #change to tracks.pop(len(tracks) - 1) to reverse song order
		print(bucket)
		random.shuffle(bucket) #shake the bucket
		print(bucket)
		while(len(bucket) > 0):
			#spotify_obj.add_to_queue(bucket.pop(0).song_id)
			stack.append(bucket.pop(0))
		bucket = []


def skip_track(): #WORKING
	track = Song(spotify_obj.currently_playing()['item']['uri'], spotify_obj)
	spotify_obj.seek_track(track.duration)

def parse_load_tracks(*args):
	uri = sys.argv[1]
	if uri == "":
		return
	print("Starting parse...")
	track_list = parse_playlist(uri)
	track_list.sort(key = lambda x: x.tempo) #sort list by tempo
	print(track_list)
	#for x in track_list:
	#	stack.append(x)
	queue_list(track_list)

parse_load_tracks()
print("The current queue is:")
print(stack)
while True:
	if len(stack) > 1:
		#temp = Song(spotify_obj.currently_playing(), spotify_obj)
		data = json.dumps(spotify_obj.current_playback(), indent=4)
		pieces = data.split()

		duration = pieces[pieces.index('"duration_ms":') + 1]
		duration = duration.replace(',', '')
		duration = int(duration)

		progress = pieces[pieces.index('"progress_ms":') + 1]
		progress = progress.replace(',', '')
		progress = int(progress)

		time_left = (duration - progress)/1000
		time_left = time_left - 15
		#print(time_left)
		if(time_left > 0):
			time.sleep(time_left)
			spotify_obj.add_to_queue(stack.pop().song_id)
			print("The current queue is:")
			print(stack)
	else:
		spotify_obj.add_to_queue(stack.pop().song_id)
		print("[[[WARNING, QUEUE ENDING]]]")


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