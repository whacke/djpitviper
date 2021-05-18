import json
class Song:

	def __init__(self, song_id, spotify):
		self.spotify = spotify
		self.song_id = song_id
		
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
		return str(self.tempo)

	def time_left(self):
		analysis = self.spotify.audio_analysis(self.song_id)
		data = json.dumps(analysis, indent=4)
		pieces = data.split()

		index = pieces.index('\'progress_ms\':')
		progress = pieces[index+1] #unfiltered tempo
		progress = progress.replace(',', '')
		progress = int(float(tempo))

		return self.duration - progress