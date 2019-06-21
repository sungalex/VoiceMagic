# Google Cloud Speech-to-Text API Long_Running example
# 긴 오디오 파일을 비동기 방식으로 처리하는 샘플
# 오디오 파일은 Google Cloud Storage에 업로드 후 사용
# 오디오 파일 크기 제한은 없으나, 전체 파일을 모두 변환 후 응답을 받을 수 있음
# https://cloud.google.com/speech-to-text/docs/async-recognize
# https://cloud.google.com/speech-to-text/docs/async-time-offsets
# Google Cloud Storage 설정 방법 : https://cloud.google.com/storage/docs/quickstart-console
"""Transcribe the given audio file asynchronously and output the word time offsets."""

import csv

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

client = speech.SpeechClient()

# gcs_uri = "gs://voice_magic_audio/경제청문회_4명인터뷰_YTN_16000.wav"    # jupyter notebook에서 Cloud Storage 한글 파일명 인식 오류
gcs_uri = "gs://voice_magic_audio/economy_4_16000.wav"

audio = types.RecognitionAudio(uri=gcs_uri)
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='ko-KR',
    enable_automatic_punctuation=True,
    enable_word_time_offsets=True)

operation = client.long_running_recognize(config, audio)

print('Waiting for operation to complete...')
response = operation.result(timeout=360)

for result in response.results:
    alternative = result.alternatives[0]
    print(u'Transcript: {}'.format(alternative.transcript))
    print('Confidence: {}'.format(alternative.confidence))

    start_time = alternative.words[0].start_time
    end_time = alternative.words[-1].end_time
    print('start_time: {} ~ end_time: {}'.format(start_time.seconds + start_time.nanos * 1e-9, \
            end_time.seconds + end_time.nanos * 1e-9))
    print()

# CSV 파일로 저장
with open('경제청문회_4명인터뷰_Transcribe.csv', 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(["start_time", "end_time", "transcript"])
    for result in response.results:
        alternative = result.alternatives[0]
        start_time = alternative.words[0].start_time.seconds + alternative.words[0].start_time.nanos * 1e-9
        end_time = alternative.words[-1].end_time.seconds + alternative.words[-1].end_time.nanos * 1e-9
        wr.writerow([start_time, end_time, alternative.transcript])

# 스크립트 만 Text 파일로 저장
with open('경제청문회_4명인터뷰_Transcribe.txt', 'w', encoding='utf-8', newline='') as f:
    for result in response.results:
        alternative = result.alternatives[0]
        f.write(alternative.transcript + " ")
