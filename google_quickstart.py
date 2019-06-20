import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


# Instantiates a client
client = speech.SpeechClient()

# Loads the audio into memory
file_name = os.path.join(os.getcwd(), 'audio_file', '홍콩행정장관사퇴거부_1명인터뷰_YTN_44100.wav')

with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()

audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code='ko-KR')

# Detects speech in the audio file
response = client.recognize(config, audio)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
