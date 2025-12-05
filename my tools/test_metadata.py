"""
Test script to verify genre metadata writing
"""
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3

mp3_file = r"c:\Users\Web developer\Documents\PROJECTS\Bot\Because He Lives (1).mp3"

try:
    # Try to read with EasyID3
    audio = EasyID3(mp3_file)
    print(f"Current metadata in {mp3_file}:")
    print(f"Genre: {audio.get('genre', 'Not set')}")
    
    # Write a test genre
    audio['genre'] = "Christian; Pop"
    audio.save()
    print("\n✓ Successfully wrote genres to file!")
    
    # Read back to verify
    audio = EasyID3(mp3_file)
    print(f"Genre after update: {audio.get('genre', 'Not set')}")
    
except Exception as e:
    print(f"Error: {e}")
    print("Trying alternative method...")
    try:
        audio = ID3(mp3_file)
        print(f"Current genre via ID3: {audio.get('TCON', 'Not set')}")
    except Exception as e2:
        print(f"Error with ID3: {e2}")
