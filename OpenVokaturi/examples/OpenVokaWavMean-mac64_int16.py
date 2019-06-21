# OpenVokaWavMean-mac64.py
# public-domain sample code by Vokaturi, 2019-05-30
#
# A sample script that uses the VokaturiPlus library to extract the emotions from
# a wav file on disk. The file has to contain a mono or stereo recording.
#
# Call syntax:
#   python3 OpenVokaWavMean-mac64.py path_to_sound_file.wav
#
# For the sound file hello.wav that comes with OpenVokaturi, the result should be:
#	Neutral: 0.760
#	Happy: 0.000
#	Sad: 0.238
#	Angry: 0.001
#	Fear: 0.000

import sys
import scipy.io.wavfile

sys.path.append("../api")
import Vokaturi

print("Loading library...")
Vokaturi.load("../lib/open/macos/OpenVokaturi-3-3-mac64.dylib")
print("Analyzed by: %s" % Vokaturi.versionAndLicense())

print("Reading sound file...")
file_name = sys.argv[1]
(sample_rate, samples) = scipy.io.wavfile.read(file_name)
print("   sample rate %.3f Hz" % sample_rate)

print("Allocating Vokaturi sample array...")
buffer_length = len(samples)
print("   %d samples, %d channels" % (buffer_length, samples.ndim))
c_buffer = Vokaturi.SampleArrayCshort(buffer_length)
if samples.ndim == 1:  # mono
	c_buffer[:] = samples[:] / 32768.0
else:  # stereo
	c_buffer[:] = (samples[:,0]+samples[:,1]) // 2

print("Creating VokaturiVoice...")
voice = Vokaturi.Voice(sample_rate, buffer_length)

print("Filling VokaturiVoice with samples...")
voice.fill_int16array(buffer_length, c_buffer)

print("Extracting emotions from VokaturiVoice...")
quality = Vokaturi.Quality()
emotionProbabilities = Vokaturi.EmotionProbabilities()
voice.extract(quality, emotionProbabilities)

if quality.valid:
	print("Neutral: %.3f" % emotionProbabilities.neutrality)
	print("Happy: %.3f" % emotionProbabilities.happiness)
	print("Sad: %.3f" % emotionProbabilities.sadness)
	print("Angry: %.3f" % emotionProbabilities.anger)
	print("Fear: %.3f" % emotionProbabilities.fear)
else:
	print("Not enough sonorancy to determine emotions")

voice.destroy()
