import json
from datetime import datetime

# Create a test song entry
test_song = {
    "Because He Lives - Newsboys": {
        "name": "Because He Lives",
        "artist": "Newsboys",
        "genres": ["Christian", "Pop"],
        "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
}

# Save to file
with open("songs_database.json", "w") as f:
    json.dump(test_song, f, indent=2)

print("Test song created successfully!")
print(json.dumps(test_song, indent=2))
