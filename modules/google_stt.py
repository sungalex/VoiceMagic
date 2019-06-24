import io
import os
import wave

# for speaker_diarization (use speech_v1p1beta1 instead speech)
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types


ENCODINGS = {
    "LINEAR16": enums.RecognitionConfig.AudioEncoding.LINEAR16,
    "FLAC": enums.RecognitionConfig.AudioEncoding.FLAC,
    "MULAW": enums.RecognitionConfig.AudioEncoding.MULAW,
    "AMR": enums.RecognitionConfig.AudioEncoding.AMR,
    "AMR_WB": enums.RecognitionConfig.AudioEncoding.AMR_WB,
    "OGG_OPUS": enums.RecognitionConfig.AudioEncoding.OGG_OPUS,
    "SPEEX_WITH_HEADER_BYTE": enums.RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE
}


def transcribe_streaming(stream_file, encoding="LINEAR16", sample_rate=16000):
    client = speech.SpeechClient()

    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]

    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        encoding=ENCODINGS[encoding],
        sample_rate_hertz=sample_rate,
        language_code='ko-KR',
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
        enable_speaker_diarization=True,    # 한국어 지원 안됨 (speaker_tag가 모두 동일인으로 분류됨)
        diarization_speaker_count=3)
    streaming_config = types.StreamingRecognitionConfig(config=config)
    
    # streaming_recognize returns a generator.
    responses = client.streaming_recognize(streaming_config, requests)
    
    words_with_tag = []
    transcripts = []

    for response in responses:
        for result in response.results:
            alternatives = result.alternatives
            for alternative in alternatives:
                print(u'Transcript: {}'.format(alternative.transcript))
                transcripts.append(alternative.transcript)    # punctuation 포함된 문장을 사용하기 위해 저장
                for words in alternative.words:
                    word = words.word
                    start_time = round(words.start_time.seconds + words.start_time.nanos * 1e-9, 3)
                    end_time = round(words.end_time.seconds + words.end_time.nanos * 1e-9, 3)
                    speaker_tag = words.speaker_tag
                    words_with_tag.append([word, start_time, end_time, speaker_tag])    # [word, start_time, end_time, speaker_tag]
            print()
    
    return words_with_tag, transcripts


def transcribe_gcs(gcs_uri, encoding="LINEAR16", sample_rate=16000):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=ENCODINGS[encoding],
        sample_rate_hertz=sample_rate,
        language_code='ko-KR',
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
        enable_speaker_diarization=True,    # 한국어 지원 안됨 (speaker_tag가 모두 동일인으로 분류됨)
        diarization_speaker_count=3)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=300)

    words_with_tag = []
    transcripts = []

    # Each result is for a consecutive portion of the audio.
    # Iterate through them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        transcripts.append(result.alternatives[0].transcript)    # punctuation 포함된 문장을 사용하기 위해 저장
        for words in result.alternative[0].words:
            word = words.word
            start_time = round(words.start_time.seconds + words.start_time.nanos * 1e-9, 3)
            end_time = round(words.end_time.seconds + words.end_time.nanos * 1e-9, 3)
            speaker_tag = words.speaker_tag
            words_with_tag.append([word, start_time, end_time, speaker_tag])    # [word, start_time, end_time, speaker_tag]
        print()
    
    return words_with_tag, transcripts


def write_wave_frames(frames, output_file, channels, sample_width, frame_rate):
    wave_stream = wave.open(output_file, 'wb')
    wave_stream.setnchannels(channels)
    wave_stream.setsampwidth(sample_width)
    wave_stream.setframerate(frame_rate)
    wave_stream.writeframes(b''.join(frames))
    wave_stream.close()
