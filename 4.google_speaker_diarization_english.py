# Google Cloud Speech-to-Text API speaker_diarization (English only)
# Google Cloud Speech-to-Text API는 en-US, en-IN, es-ES 언어의 화자 분할을 지원합니다. (한국어 미지원)
# https://cloud.google.com/speech-to-text/docs/multiple-voices
# 화자 분리 API는 베타 버전 입니다.
# google.cloud.speech_v1p1beta1.SpeechClient().streaming_recognize(streaming_config, requests)

import io
import os

from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

stream_file = os.path.join(os.getcwd(), 'audio_file', 'commercial_mono.wav')

with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

# In practice, stream should be a generator yielding chunks of audio data.
stream = [content]

requests = (speech.types.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in stream)

config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=8000,
    language_code='en-US',
    enable_speaker_diarization=True,
    diarization_speaker_count=2,
    enable_automatic_punctuation=True,
    enable_word_time_offsets=True,
    model='default')

streaming_config = speech.types.StreamingRecognitionConfig(config=config)

# streaming_recognize returns a generator.
responses = client.streaming_recognize(streaming_config, requests)

for response in responses:
    # Once the transcription has settled, the first result will contain the is_final result. 
    # The other results will be for subsequent portions of the audio.

    for result in response.results:
        print('Finished: {}'.format(result.is_final))
        print('Stability: {}'.format(result.stability))
        alternatives = result.alternatives
        # The alternatives are ordered from most likely to least.
        for alternative in alternatives:
            print('Confidence: {}'.format(alternative.confidence))
            print(u'Transcript: {}'.format(alternative.transcript))
            
            print('Speaker:(누적)', end=" ")
            for words in alternative.words:
                print(words.speaker_tag, end=" ")
            print()
