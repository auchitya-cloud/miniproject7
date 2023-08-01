
# Install required libraries !pip install SpeechRecognition pydub

import speech_recognition as sr
import os 
import subprocess
from google.colab import files
from pydub import AudioSegment
from pydub.silence import split_on_silence

files.upload()
subprocess.call(['ffmpeg', '-i', 'audio_file.mp3','wav_file.wav'])

# Initialize the recognizer
r = sr.Recognizer()

# A function that splits the audio file into chunks
# and applies speech recognition
def get_audio_transcription(path):
    """
    Splitting the audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # Open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # Split audio sound where silence is 700 milliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # Experiment with this value for your target audio file
        min_silence_len=500,
        # Adjust this per requirement
        silence_thresh=sound.dBFS-14,
        # Keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # Create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # Process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # Export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # Recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # Try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # Return the text for all chunks detected
    return whole_text

path = "/content/wav_file.wav"
print("\nUncovered Message:", get_audio_transcription(path))
