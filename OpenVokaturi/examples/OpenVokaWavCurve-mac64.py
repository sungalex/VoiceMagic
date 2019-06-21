# OpenVokaWavCurve-mac64.py
# public-domain sample code by Vokaturi, 2019-05-30
#
# A sample script that uses the OpenVokaturi library to extract the emotions from
# a wav file on disk. The file has to contain a mono or stereo recording.
#
# Call syntax:
#   python3 OpenVokaWavCurve-mac64.py path_to_sound_file.wav

import sys
import scipy.io.wavfile

sys.path.append("../api")
import Vokaturi

print ("Loading library...")
Vokaturi.load("../lib/open/macos/OpenVokaturi-3-3-mac64.dylib")
print ("Analyzed by: %s" % Vokaturi.versionAndLicense())

print ("Reading sound file...")
file_name = sys.argv[1]
(sample_rate, samples) = scipy.io.wavfile.read(file_name)
print ("   sample rate %.3f Hz" % sample_rate)

print ("Allocating Vokaturi sample array...")
buffer_length = len(samples)
print ("   %d samples, %d channels" % (buffer_length, samples.ndim))
c_buffer = Vokaturi.SampleArrayC(sample_rate)
print ("Creating VokaturiVoice...")
voice = Vokaturi.Voice (sample_rate, buffer_length)

numberOfSeconds = int (buffer_length / sample_rate)
print ("Start(s) End(s) Neutral Happy Sad Angry Fear")

for isecond in range(0, numberOfSeconds):
	startSample = round(isecond*sample_rate)
	endSample = round((isecond+1)*sample_rate)
	print (startSample, endSample)
	if samples.ndim == 1:  # mono
		c_buffer[:] = samples[startSample:endSample] / 32768.0
	else:  # stereo
		c_buffer[:] = 0.5*(samples[startSample:endSample,0]+0.0+samples[startSample:endSample,1]) / 32768.0

	voice.fill(sample_rate, c_buffer)

	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voice.extract(quality, emotionProbabilities)

	if quality.valid:
		print (isecond, isecond + 1,
			"%.3f" % emotionProbabilities.neutrality,
			"%.3f" % emotionProbabilities.happiness,
			"%.3f" % emotionProbabilities.sadness,
			"%.3f" % emotionProbabilities.anger,
			"%.3f" % emotionProbabilities.fear)

voice.destroy()
