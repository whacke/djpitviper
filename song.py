import json
class Song:

	def __init__(self, song_obj, spotify):
		self.spotify = spotify
		self.song_obj = song_obj
		self.song_id = song_obj['uri']
		
		analysis = self.spotify.audio_analysis(self.song_id)
		data = json.dumps(analysis, indent=4)
		pieces = data.split()

		index = pieces.index('"tempo":')
		tempo = pieces[index+1] #unfiltered tempo
		tempo = tempo.replace(',', '')
		self.tempo = int(float(tempo))

		index = pieces.index('"duration":')
		duration = pieces[index+1] #unfiltered duration
		duration = duration.replace(',', '')
		self.duration = int((float(duration) - 11) * 1000)

	def __repr__(self):
		return self.song_obj['name']
