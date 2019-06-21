# Google Cloud Speech-to-Text API Streaming example
# 1분 이상의 긴 오디오 파일을 Streaming 방식으로 처리하는 샘플
# https://cloud.google.com/speech-to-text/docs/streaming-recognize
# google.cloud.speech.SpeechClient().streaming_recognize(streaming_config, requests)
# Audio file size limit : 10M bytes

def transcribe_streaming(stream_file):
    import io

    """Streams transcription of the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    
    client = speech.SpeechClient()

    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]

    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR',
        enable_automatic_punctuation=True)
    streaming_config = types.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print(u'Transcript: {}'.format(alternative.transcript))

if __name__ == '__main__':
    import os

    # Request payload size limit: 10485760 bytes
    stream_file = os.path.join(os.getcwd(), 'audio_file', '황금종려상자랑봉준호_3명인터뷰_YTN_16000.wav')
    transcribe_streaming(stream_file)
