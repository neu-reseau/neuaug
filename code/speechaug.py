import sys
import os
import random
import numpy as np
from pydub import AudioSegment
from pydub.generators import WhiteNoise, PinkNoise, BrownNoise

def add_noise(audio, noise_type, noise_level):
    duration_ms = len(audio)
    if noise_type == 'white':
        noise = WhiteNoise().to_audio_segment(duration=duration_ms)
    elif noise_type == 'pink':
        noise = PinkNoise().to_audio_segment(duration=duration_ms)
    elif noise_type == 'brown':
        noise = BrownNoise().to_audio_segment(duration=duration_ms)
    else:
        raise ValueError("Invalid noise type")
    
    noise = noise - (noise.dBFS - audio.dBFS - noise_level)
    return audio.overlay(noise)

def time_stretch(audio, rate):
    return audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * rate)
    }).set_frame_rate(audio.frame_rate)

def pitch_shift(audio, semitones):
    new_sample_rate = int(audio.frame_rate * (2 ** (semitones / 12)))
    return audio._spawn(audio.raw_data, overrides={
        "frame_rate": new_sample_rate
    }).set_frame_rate(audio.frame_rate)

def augment_audio(audio):
    augmentations = [
        lambda a: add_noise(a, random.choice(['white', 'pink', 'brown']), random.uniform(-20, -10)),
        lambda a: time_stretch(a, random.uniform(0.9, 1.1)),
        lambda a: pitch_shift(a, random.uniform(-2, 2))
    ]
    return random.choice(augmentations)(audio)

def main(input_folder, output_folder, num_augmentations):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.mp3'):
            input_path = os.path.join(input_folder, filename)
            audio = AudioSegment.from_mp3(input_path)
            
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_original.mp3")
            audio.export(output_path, format="mp3")
            
            for i in range(num_augmentations):
                augmented_audio = augment_audio(audio)
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_aug_{i+1}.mp3")
                augmented_audio.export(output_path, format="mp3")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python audio_augment.py <input folder> <output folder> <number of augmented samples per audio>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    num_augmentations = int(sys.argv[3])

    main(input_folder, output_folder, num_augmentations)