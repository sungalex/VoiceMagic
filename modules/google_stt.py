import io
import os
import sys
import re
import wave

# for speaker_diarization (use speech_v1p1beta1 instead speech)
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

# from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types

import pyaudio

from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


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
    
    words_with_tags = []
    transcripts = []

    print("Waiting for transcribe...")
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
                    words_with_tags.append([word, start_time, end_time, speaker_tag])    # [word, start_time, end_time, speaker_tag]
            print()    # newline
    
    return words_with_tags, transcripts


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

    words_with_tags = []
    transcripts = []

    # Each result is for a consecutive portion of the audio.
    # Iterate through them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        transcripts.append(result.alternatives[0].transcript)    # punctuation 포함된 문장을 사용하기 위해 저장
        for words in result.alternatives[0].words:
            word = words.word
            start_time = round(words.start_time.seconds + words.start_time.nanos * 1e-9, 3)
            end_time = round(words.end_time.seconds + words.end_time.nanos * 1e-9, 3)
            speaker_tag = words.speaker_tag
            words_with_tags.append([word, start_time, end_time, speaker_tag])    # [word, start_time, end_time, speaker_tag]
        print()
    
    return words_with_tags, transcripts


def write_wave_frames(frames, output_file, channels, sample_width, frame_rate):
    wave_stream = wave.open(output_file, 'wb')
    wave_stream.setnchannels(channels)
    wave_stream.setsampwidth(sample_width)
    wave_stream.setframerate(frame_rate)
    wave_stream.writeframes(b''.join(frames))
    wave_stream.close()


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk, wf, stream):
        self._rate = rate
        self._chunk = chunk
        self.wf = wf
        self.output_stream = stream

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
#         self._buff.put(in_data)
        data = self.wf.readframes(frame_count)
        self._buff.put(data)
        self.output_stream.write(data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def microphone_streaming_start(wf, output_stream):
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'ko-KR'

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True)
    #     enable_speaker_diarization=True,
    #     diarization_speaker_count=3)

    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK, wf, output_stream) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)
