from pydub import AudioSegment

sound = AudioSegment.from_mp3("speech.mp3")
sound.export("wvfile.wav", format="wav")