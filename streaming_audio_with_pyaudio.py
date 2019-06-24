# !conda install portaudio
# !brew install portaudio    # for mac
# !pip install pyaudio

try:
    import pyaudio
    import numpy as np
    import wave
except Exception as e:
    print("Something didn't import.\n => {}".format(e))

CHUNK = 1024   # 1024 bytes of data read from the buffer
WAVE_OUTPUT_FILENAME = "audio_file/pyaudio_output_16000.wav"

wf = wave.open("audio_file/bong_interview_YTN_16000.wav", 'rb')

# instantiate PyAudio (1)
audio = pyaudio.PyAudio()

# open stream (2)
FORMAT=audio.get_format_from_width(wf.getsampwidth())
CHANNELS=wf.getnchannels()
RATE=wf.getframerate()

stream = audio.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)

# read data
frames = []
data = wf.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    frames.append(data)
    stream.write(data)
    data = wf.readframes(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# write audio to file (5)
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

# close PyAudio (6)
audio.terminate()
