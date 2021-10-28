import pyaudio
import wave

# This is the card number for your speaker
# You can get this by running aplay -l
SPEAKER_CARD_NUMBER = 2

# Create an audio device
audio = pyaudio.PyAudio()

# Open the spooky-sound.wav audio file
with wave.open('spooky-sound.wav', 'rb') as wave_file:
    # Create an audio output stream using the wudio format from the wave file that has just been opened
    # This will output to the SPEAKER_CARD_NUMBER speaker
    stream = audio.open(format=audio.get_format_from_width(wave_file.getsampwidth()),
                        channels=wave_file.getnchannels(),
                        rate=wave_file.getframerate(),
                        output_device_index=SPEAKER_CARD_NUMBER,
                        output=True)

    # Read data from the wave file
    data = wave_file.readframes(4096)

    # All the while we have data, write it to the audio stream
    while len(data) > 0:
        # Write the data to the output stream. This blocks until the stream has been played
        stream.write(data)
        # Read more data. Once the end of the stream is reached the data will be empty and
        # the loop will exit
        data = wave_file.readframes(4096)

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()