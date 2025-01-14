import speech_recognition as sr
from pydub import AudioSegment
import os
from fuzzywuzzy import process
import audioread
import wave

def convert_mp3_to_wav(directory):
    # Check and create a directory for the WAV files
    wav_directory = os.path.join(directory, "wav_files")
    if not os.path.exists(wav_directory):
        os.makedirs(wav_directory)

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.mp3'):
            mp3_path = os.path.join(directory, filename)
            wav_path = os.path.join(wav_directory, os.path.splitext(filename)[0] + '.wav')
            with audioread.audio_open(mp3_path) as source:
                with wave.open(wav_path, 'w') as dest:
                    dest.setnchannels(source.channels)
                    dest.setsampwidth(2)  # Assumes 16-bit audio
                    dest.setframerate(source.samplerate)

                    for buffer in source:
                        dest.writeframes(buffer)


# Paths to the directories
patient_names_dir = 'patient_names'
provider_names_dir = 'provider_names'

# Convert all MP3 files in both directories
convert_mp3_to_wav(patient_names_dir)
convert_mp3_to_wav(provider_names_dir)

def read_rttm(file_path):
    segments = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            start_time = float(parts[3]) * 1000  # Convert to milliseconds
            duration = float(parts[4]) * 1000  # Convert to milliseconds
            speaker_id = parts[7]
            segments.append((start_time, duration, speaker_id))
    return segments


def load_names(directory):
    names = []
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            # Assumes the file format is 'Firstname_Lastname.wav'
            firstname = filename.split('_')[0]
            names.append(firstname)
    return names

def find_best_match(word, names):
    highest = process.extractOne(word, names)
    if highest and highest[1] >= 95:
        return highest[0]
    return word

def transcribe_audio(audio_path, segments, output_file_path):
    recognizer = sr.Recognizer()
    audio_full = AudioSegment.from_wav(audio_path)

    provider_names = load_names('provider_names')
    patient_names = load_names('patient_names')
    all_names = set(provider_names + patient_names)

    # Ensure the 'transcripts' folder exists
    transcripts_folder = 'src/transcripts'
    os.makedirs(transcripts_folder, exist_ok=True)

    with open(output_file_path, 'w') as output_file:
        current_speaker = None
        for i, (start_time, duration, speaker_id) in enumerate(segments):
            if current_speaker != speaker_id:
                if current_speaker is not None:
                    output_file.write("\n")  # Start a new line for a new speaker
                output_file.write(f"{speaker_id}: ")
                current_speaker = speaker_id
            segment_audio = audio_full[start_time:start_time + duration]
            segment_file_path = f"temp_segment_{i}.wav"
            segment_audio.export(segment_file_path, format="wav")  # Save segment

            with sr.AudioFile(segment_file_path) as source:
                audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio)
                    words = text.split()
                    corrected_text = ' '.join([find_best_match(word, all_names) for word in words])
                    output_file.write(corrected_text + " ")
                except sr.UnknownValueError:
                    output_file.write("[Unintelligible] ")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}", file=output_file)

            os.remove(segment_file_path)  # Clean up the temporary file

    print(f"Transcript saved to {output_file_path}")

# Example usage
# rttm_file_path = 'audio.rttm'
# audio_file_path = 'audioFiles/example.wav'
# segments = read_rttm(rttm_file_path)
# output_file_path = transcribe_audio(audio_file_path, segments)

#transcript = transcribe_audio(audio_file_path, segments)
#print(transcript)

def process_all_rttm_files(rttm_directory, audio_files_directory, transcripts_directory):
    # Ensure the transcripts directory exists
    os.makedirs(transcripts_directory, exist_ok=True)

    # Loop through all RTTM files in the 'rttm' directory
    for rttm_filename in os.listdir(rttm_directory):
        if rttm_filename.endswith(".rttm"):
            # Construct the full path to the current RTTM file
            rttm_file_path = os.path.join(rttm_directory, rttm_filename)

            # Correctly associate the RTTM file with its corresponding audio file
            base_name = os.path.splitext(rttm_filename)[0].replace('_rttm', '')  # Remove '_rttm' from the RTTM filename
            audio_file_path = os.path.join(audio_files_directory, f"{base_name}.wav")

            # Check if the corresponding audio file exists
            if os.path.exists(audio_file_path):
                # Read segments from the RTTM file
                segments = read_rttm(rttm_file_path)

                # Adjust the transcribe_audio function to accept the output_file_path parameter
                output_file_path = os.path.join(transcripts_directory, f"{base_name}_transcript.txt")
                transcribe_audio(audio_file_path, segments,
                                 output_file_path)  # Make sure this function accepts the output file path
                print(f"Transcript for {base_name} saved to {output_file_path}")
            else:
                print(f"Audio file for {rttm_filename} not found in {audio_files_directory}")


# Example usage
