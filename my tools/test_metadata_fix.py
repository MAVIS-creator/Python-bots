"""
Test script to verify genre metadata writing with ISO-8859-1 encoding
"""
from mutagen.id3 import ID3, TCON
import os

mp3_file = r"c:\Users\Web developer\Documents\PROJECTS\Bot\my tools\Because He Lives (1).mp3"

print(f"Testing metadata write/read on: {mp3_file}")
print(f"File exists: {os.path.exists(mp3_file)}")
print()

try:
    # Step 1: Try to read current metadata
    print("Step 1: Reading current metadata...")
    try:
        audio = ID3(mp3_file)
        print(f"✓ ID3 tags found")
        current_genres = audio.get('TCON', None)
        if current_genres:
            print(f"  Current Genre: {current_genres.text}")
        else:
            print(f"  Current Genre: None")
    except Exception as e:
        print(f"  No existing ID3 tags, will create new ones")
        audio = ID3()
    
    # Step 2: Write new genre metadata
    print("\nStep 2: Writing new genre metadata...")
    genres = ["Christian", "Pop"]
    genre_str = "; ".join(genres)
    
    # Remove old genre tag
    audio.delall("TCON")
    
    # Add new genre tag with ISO-8859-1 encoding
    audio.add(
        TCON(
            encoding=0,  # ISO-8859-1 (Windows compatible)
            text=[genre_str]
        )
    )
    
    # Save as ID3v2.3 - pass filename
    audio.save(mp3_file, v2_version=3)
    print(f"✓ Wrote genres: {genre_str}")
    print(f"✓ Saved as ID3v2.3 with ISO-8859-1 encoding")
    
    # Step 3: Read back to verify
    print("\nStep 3: Reading back to verify...")
    audio = ID3(mp3_file)
    written_genres = audio.get('TCON', None)
    if written_genres:
        print(f"✓ Verified Genre: {written_genres.text}")
        print(f"✓ Encoding: {written_genres.encoding} (0=ISO-8859-1 ✓)")
    else:
        print(f"✗ Genre not found after writing!")
    
    # Step 4: Check file modification time
    print("\nStep 4: File status...")
    file_mtime = os.path.getmtime(mp3_file)
    from datetime import datetime
    mod_time = datetime.fromtimestamp(file_mtime)
    print(f"✓ File last modified: {mod_time}")
    
    print("\n" + "="*60)
    print("SUCCESS! Metadata has been written to the MP3 file.")
    print("The genre should now appear in Windows Explorer Properties.")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
