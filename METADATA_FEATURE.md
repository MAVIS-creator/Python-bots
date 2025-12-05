# Music Genre Bot - Metadata Writing Feature

## What's New

The bot now **automatically writes genre metadata directly into MP3 files** so the genres appear in:
- ✅ Windows File Explorer Properties (Details tab)
- ✅ Windows Media Player
- ✅ Other audio players that read ID3 tags
- ✅ Your songs_database.json file (backup)

## How It Works

### When You Import Songs:
1. Select songs to import
2. Choose genres for each song (or use "Batch Apply to All")
3. Click "Save All Songs"
4. **The bot automatically writes the genres to the MP3 file's metadata**
5. You'll see the success message: "Genre metadata has been written to the files"

### The Metadata Writing Process:
- Converts your selected genres to ID3 tags (MP3 standard)
- Uses the format: "Genre1; Genre2; Genre3" (semicolon-separated)
- Writes directly to the file using the `mutagen` library
- Handles both EasyID3 (simple) and ID3 (advanced) formats

## Example
If you select "Christian" and "Pop" for a song, the MP3 file will have:
- **Genre**: "Christian; Pop"

This will appear in Windows Properties → Details tab → Genre field.

## Requirements
- mutagen library (already installed)
- MP3 files (other formats like FLAC, WAV may need additional setup)

## Testing the Feature
1. Import an MP3 file
2. Select genres and save
3. Right-click the MP3 file in File Explorer
4. Select Properties → Details tab
5. Look for the "Genre" field - it should show your selected genres!
