from pydub import AudioSegment
import speech_recognition as sr
from pyannote.audio import Pipeline
from pyannote.core import Segment
from pyannote.audio import Audio
import os

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token="USEYOUROWNYOUTHIEF")

def mp3_to_wav(audio_file_path):
    sound = AudioSegment.from_mp3(audio_file_path)
    wav_file_path = audio_file_path.replace(".mp3", ".wav")
    sound.export(wav_file_path, format="wav")
    return wav_file_path


def get_segmentation():
    audio_files_directory = "src/audioFiles"
    rttm_directory = 'src/rttm'
    os.makedirs(rttm_directory, exist_ok=True)
    for mp3_filename in os.listdir(audio_files_directory):
        if mp3_filename.endswith(".mp3"):
            mp3_file_path = os.path.join(audio_files_directory, mp3_filename)
            wav_file = mp3_to_wav(mp3_file_path)  # Convert MP3 to WAV

            # excerpt = Segment(start=0.0, end=10.0)
            # waveform, sample_rate = Audio().crop(wav_file, excerpt)
            # diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})
            diarization = pipeline(wav_file, min_speakers=2, max_speakers=5)

            # Generate RTTM filename by adding '_rttm' before the file extension
            base_name = os.path.splitext(os.path.basename(wav_file))[
                0]  # Get the base name of the WAV file (without extension)
            rttm_filename = f"{base_name}_rttm.rttm"  # Append '_rttm' to the base name and add '.rttm' extension

            # Construct the full path to save the RTTM file within the 'rttm' directory
            rttm_file_path = os.path.join(rttm_directory, rttm_filename)

            with open(rttm_file_path, "w") as rttm_file:
                diarization.write_rttm(rttm_file)

            print(f"RTTM file saved to {rttm_file_path}")
