"""
Direct test of the bot's write_genre_to_file function
"""
import sys
sys.path.insert(0, r"c:\Users\Web developer\Documents\PROJECTS\Bot")

from music_genre_bot import MusicGenreBot
import tkinter as tk
from mutagen.id3 import ID3

# Create a dummy root window (bot needs it to initialize)
root = tk.Tk()
root.withdraw()  # Hide the window

# Create bot instance
bot = MusicGenreBot(root)

mp3_file = r"c:\Users\Web developer\Documents\PROJECTS\Bot\my tools\Because He Lives (1).mp3"

print("="*60)
print("Testing bot's write_genre_to_file() function")
print("="*60)

# Test writing genres
test_genres = ["Christian", "Pop", "Phonk"]
print(f"\nWriting genres: {test_genres}")
result = bot.write_genre_to_file(mp3_file, test_genres)

if result:
    print("✓ Write successful!")
    
    # Verify by reading
    print("\nVerifying metadata...")
    audio = ID3(mp3_file)
    written_genres = audio.get('TCON', None)
    
    if written_genres:
        print(f"✓ Genre tag found: {written_genres.text}")
        print(f"✓ Encoding: {written_genres.encoding} (LATIN1/ISO-8859-1 ✓)")
        print("\n" + "="*60)
        print("SUCCESS! Metadata is correctly written.")
        print("Check the file in Windows Explorer Properties → Details")
        print("="*60)
    else:
        print("✗ Genre tag not found after write!")
else:
    print("✗ Write failed!")

root.destroy()
