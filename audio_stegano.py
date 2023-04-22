import wave
import numpy as np

def encode_lsb_audio(audio_file_path, message):
    audio = wave.open(audio_file_path, 'r')
    params = audio.getparams()
    frames = audio.readframes(audio.getnframes())

    audio_array = np.frombuffer(frames, dtype=np.int16)
    message_binary = ''.join(format(ord(c), '08b') for c in message)

    message_binary += '00000000'

    if len(message_binary) > len(audio_array):
        raise ValueError('Message is too long to fit in the audio file')

    audio_array_copy = audio_array.copy()
    audio_array_copy.setflags(write=True)

    for i in range(len(message_binary)):
        audio_array_copy[i] &= ~1  # Clear the least significant bit
        audio_array_copy[i] |= int(message_binary[i])

    encoded_frames = audio_array_copy.tobytes()

    encoded_audio = wave.open('img/encoded_audio.wav', 'w')
    encoded_audio.setparams(params)
    encoded_audio.writeframes(encoded_frames)
    encoded_audio.close()

    print('Message successfully encoded in audio file.')

def decode_lsb_audio(encoded_audio_file_path):
    # Open the encoded audio file
    encoded_audio = wave.open(encoded_audio_file_path, 'r')
    params = encoded_audio.getparams()
    frames = encoded_audio.readframes(encoded_audio.getnframes())

    encoded_audio_array = np.frombuffer(frames, dtype=np.int16)

    message_binary = ''
    for sample in encoded_audio_array:
        message_binary += str(sample & 1)

    # Convert the binary message to ASCII characters
    message = ''
    for i in range(0, len(message_binary), 8):
        byte = message_binary[i:i + 8]
        if byte == '00000000':
            break
        char = chr(int(byte, 2))
        message += char

    return message.strip()


if __name__ == '__main__':
    encode_lsb_audio("img/audio.wav",input("Message:"))
    print(decode_lsb_audio("img/encoded_audio.wav"))
