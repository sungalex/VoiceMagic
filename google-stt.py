#!/usr/bin/env python

def google_stt(gcs_uri, speakers=1, hertz=16000):
    # Imports the Google Cloud client library
    from google.cloud import speech_v1p1beta1 as speech    # speaker_diarization
    from google.cloud.speech_v1p1beta1 import enums
    from google.cloud.speech_v1p1beta1 import types

    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    audio = types.RecognitionAudio(uri=gcs_uri)
    
    if speakers == 1:
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=hertz,
            language_code='ko-KR')
    else:
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=hertz,
            language_code='ko-KR',
            enable_speaker_diarization=True,
            diarization_speaker_count=speakers)
    
    response = client.long_running_recognize(config, audio)
    
    # Printing out the output:
    for result in response.result().results:
        print("time:", result.alternatives[0].words[0].start_time.seconds, "~",\
            result.alternatives[0].words[-1].end_time.seconds)
        print("transcript:", result.alternatives[0].transcript)
        print("confidence:", result.alternatives[0].confidence)


if __name__ == '__main__':
    uri = "gs://voice_magic_audio/황금종려상자랑봉준호_3명인터뷰_YTN_16000.wav"
    google_stt(gcs_uri=uri, speakers=3, hertz=16000)
