import pygame
import numpy as np
import os
import random

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Create sounds directory if it doesn't exist
if not os.path.exists("sounds"):
    os.makedirs("sounds")

def generate_sine_wave(freq, duration, volume=0.5):
    """Generate a sine wave at the given frequency, duration, and volume"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    wave = np.sin(freq * t * 2 * np.pi)
    # Apply volume and fade out
    wave = wave * volume
    fade_samples = int(0.1 * sample_rate)  # 100ms fade out
    if len(wave) > fade_samples:
        fade_out = np.linspace(1.0, 0.0, fade_samples)
        wave[-fade_samples:] *= fade_out
    # Convert to 16-bit signed integers
    wave = np.int16(wave * 32767)
    # Make stereo by duplicating the mono channel
    stereo = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound(stereo)

def save_wave_to_file(wave_array, filename, sample_rate=44100):
    """Save a numpy array as a WAV file"""
    try:
        from scipy.io import wavfile
        wavfile.write(filename, sample_rate, wave_array)
    except ImportError:
        # Fallback to wave module if scipy is not available
        import wave as wave_module
        with wave_module.open(filename, 'wb') as wave_file:
            wave_file.setnchannels(2)  # Stereo
            wave_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wave_file.setframerate(sample_rate)
            wave_file.writeframes(wave_array.tobytes())

def generate_jump_sound():
    """Generate a jump sound effect"""
    print("Generating jump sound...")
    # Start at a higher frequency and slide down
    sample_rate = 44100
    duration = 0.3
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Frequency slide from high to low
    freq = np.linspace(800, 400, len(t))
    wave = np.sin(freq * t * 2 * np.pi)
    
    # Apply envelope
    envelope = np.exp(-5 * t)
    wave = wave * envelope * 0.7
    
    # Convert to 16-bit signed integers
    wave = np.int16(wave * 32767)
    
    # Make stereo by duplicating the mono channel
    stereo = np.column_stack((wave, wave))
    
    # Save to file directly
    save_wave_to_file(stereo, os.path.join("sounds", "jump.wav"))
    print("Jump sound saved.")

def generate_boost_sound():
    """Generate a boost jump sound effect"""
    print("Generating boost sound...")
    sample_rate = 44100
    duration = 0.4
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Frequency slide from low to high
    freq = np.linspace(300, 1200, len(t))
    wave = np.sin(freq * t * 2 * np.pi)
    
    # Add a second tone
    wave2 = np.sin((freq * 1.5) * t * 2 * np.pi) * 0.5
    wave = wave + wave2
    
    # Apply envelope
    envelope = np.exp(-4 * t)
    wave = wave * envelope * 0.8
    
    # Convert to 16-bit signed integers
    wave = np.int16(wave * 32767)
    
    # Make stereo by duplicating the mono channel
    stereo = np.column_stack((wave, wave))
    
    # Save to file directly
    save_wave_to_file(stereo, os.path.join("sounds", "boost.wav"))
    print("Boost sound saved.")

def generate_land_sound():
    """Generate a landing sound effect"""
    print("Generating land sound...")
    sample_rate = 44100
    duration = 0.2
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Low frequency thud
    freq = 150
    wave = np.sin(freq * t * 2 * np.pi)
    
    # Add some noise
    noise = np.random.uniform(-0.2, 0.2, len(t))
    wave = wave + noise
    
    # Apply envelope
    envelope = np.exp(-10 * t)
    wave = wave * envelope * 0.6
    
    # Convert to 16-bit signed integers
    wave = np.int16(wave * 32767)
    
    # Make stereo by duplicating the mono channel
    stereo = np.column_stack((wave, wave))
    
    # Save to file directly
    save_wave_to_file(stereo, os.path.join("sounds", "land.wav"))
    print("Land sound saved.")

def generate_game_over_sound():
    """Generate a game over sound effect"""
    print("Generating game over sound...")
    sample_rate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Descending notes
    notes = [440, 392, 349, 330, 294]
    note_duration = duration / len(notes)
    wave = np.zeros_like(t)
    
    for i, note in enumerate(notes):
        start = int(i * note_duration * sample_rate)
        end = int((i + 1) * note_duration * sample_rate)
        if end > len(t):
            end = len(t)
        t_segment = t[start:end] - (i * note_duration)
        wave[start:end] = np.sin(note * t_segment * 2 * np.pi)
    
    # Apply envelope
    envelope = np.exp(-2 * t)
    wave = wave * envelope * 0.9
    
    # Convert to 16-bit signed integers
    wave = np.int16(wave * 32767)
    
    # Make stereo by duplicating the mono channel
    stereo = np.column_stack((wave, wave))
    
    # Save to file directly
    save_wave_to_file(stereo, os.path.join("sounds", "gameover.wav"))
    print("Game over sound saved.")

def generate_background_music():
    """Generate simple background music"""
    print("Generating background music...")
    sample_rate = 44100
    duration = 10.0  # 10 seconds of music that will loop
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Base frequencies for a simple melody
    melody_notes = [262, 294, 330, 349, 392, 440, 494, 523]  # C4 to C5
    chord_notes = [262, 330, 392]  # C major chord
    
    # Create a simple melody
    melody = np.zeros_like(t)
    chord = np.zeros_like(t)
    
    # Divide into measures
    measures = 8
    measure_duration = duration / measures
    notes_per_measure = 4
    note_duration = measure_duration / notes_per_measure
    
    for measure in range(measures):
        for note in range(notes_per_measure):
            start = int((measure * measure_duration + note * note_duration) * sample_rate)
            end = int((measure * measure_duration + (note + 0.9) * note_duration) * sample_rate)
            if end > len(t):
                end = len(t)
                
            # Choose a random note from the melody
            melody_freq = melody_notes[random.randint(0, len(melody_notes)-1)]
            t_segment = t[start:end] - (measure * measure_duration + note * note_duration)
            melody[start:end] = np.sin(melody_freq * t_segment * 2 * np.pi) * 0.3
            
            # Add a chord every first beat
            if note == 0:
                for chord_note in chord_notes:
                    chord[start:end] += np.sin(chord_note * t_segment * 2 * np.pi) * 0.1
    
    # Combine melody and chord
    wave = melody + chord
    
    # Apply a gentle envelope to each note to avoid clicks
    for measure in range(measures):
        for note in range(notes_per_measure):
            start = int((measure * measure_duration + note * note_duration) * sample_rate)
            end = int((measure * measure_duration + (note + 1) * note_duration) * sample_rate)
            if end > len(t):
                end = len(t)
                
            # Apply attack and release
            attack_samples = int(0.01 * sample_rate)  # 10ms attack
            release_samples = int(0.05 * sample_rate)  # 50ms release
            
            if end - start > attack_samples + release_samples:
                # Attack
                attack = np.linspace(0.0, 1.0, attack_samples)
                wave[start:start+attack_samples] *= attack
                
                # Release
                release = np.linspace(1.0, 0.0, release_samples)
                wave[end-release_samples:end] *= release
    
    # Convert to 16-bit signed integers
    wave = np.int16(wave * 32767)
    
    # Make stereo by duplicating the mono channel
    stereo = np.column_stack((wave, wave))
    
    # Save to file directly
    save_wave_to_file(stereo, os.path.join("sounds", "background.wav"))
    print("Background music saved.")

if __name__ == "__main__":
    print("Generating sound effects...")
    generate_jump_sound()
    generate_boost_sound()
    generate_land_sound()
    generate_game_over_sound()
    generate_background_music()
    print("All sound effects generated successfully!")
    print("You can now run the game with sound.")
