import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import os
from datetime import datetime

class MusicGenreBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Genre Manager Bot")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Data file
        self.data_file = "songs_database.json"
        self.songs = self.load_songs()
        
        # Available genres
        self.genres = ["Phonk", "Christian", "Pop", "Rock", "Hip-Hop", "Jazz", "Electronic", "R&B", "Country", "Metal"]
        
        self.setup_ui()
        
    def load_songs(self):
        """Load songs from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_songs(self):
        """Save songs to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.songs, f, indent=2)
    
    def setup_ui(self):
        """Create the user interface"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), background="#f0f0f0")
        style.configure('TLabel', font=('Helvetica', 10), background="#f0f0f0")
        style.configure('TButton', font=('Helvetica', 10))
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎵 Music Genre Manager Bot", style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Add/Update Song", padding=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Song Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.song_name_entry = ttk.Entry(input_frame, width=40)
        self.song_name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(input_frame, text="Artist:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.artist_entry = ttk.Entry(input_frame, width=40)
        self.artist_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(input_frame, text="Genres (select multiple):").grid(row=2, column=0, sticky=tk.NW, pady=5)
        
        # Genre selection frame
        genre_frame = ttk.Frame(input_frame)
        genre_frame.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        self.genre_vars = {}
        for i, genre in enumerate(self.genres):
            var = tk.BooleanVar()
            self.genre_vars[genre] = var
            checkbox = ttk.Checkbutton(genre_frame, text=genre, variable=var)
            checkbox.grid(row=i//3, column=i%3, sticky=tk.W, padx=5)
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add/Update Song", command=self.add_song).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Import from File", command=self.import_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        # Display section
        display_frame = ttk.LabelFrame(main_frame, text="Your Music Library", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create Treeview
        columns = ("Song", "Artist", "Genres")
        self.tree = ttk.Treeview(display_frame, columns=columns, height=12)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Song", anchor=tk.W, width=250)
        self.tree.column("Artist", anchor=tk.W, width=200)
        self.tree.column("Genres", anchor=tk.W, width=250)
        
        self.tree.heading("#0", text="")
        self.tree.heading("Song", text="Song Name")
        self.tree.heading("Artist", text="Artist")
        self.tree.heading("Genres", text="Genres")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Delete Selected", command=self.delete_song).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Edit Selected", command=self.edit_song).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Refresh", command=self.refresh_display).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Export to CSV", command=self.export_csv).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready | Total Songs: 0")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=5)
        
        self.refresh_display()
    
    def add_song(self):
        """Add or update a song"""
        song_name = self.song_name_entry.get().strip()
        artist = self.artist_entry.get().strip()
        selected_genres = [genre for genre, var in self.genre_vars.items() if var.get()]
        
        if not song_name:
            messagebox.showwarning("Input Error", "Please enter a song name!")
            return
        
        if not artist:
            messagebox.showwarning("Input Error", "Please enter an artist name!")
            return
        
        if not selected_genres:
            messagebox.showwarning("Input Error", "Please select at least one genre!")
            return
        
        # Create song key
        song_key = f"{song_name} - {artist}"
        
        # Add to database
        self.songs[song_key] = {
            "name": song_name,
            "artist": artist,
            "genres": selected_genres,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.save_songs()
        messagebox.showinfo("Success", f"Song '{song_name}' has been added/updated!")
        self.clear_fields()
        self.refresh_display()
    
    def clear_fields(self):
        """Clear input fields"""
        self.song_name_entry.delete(0, tk.END)
        self.artist_entry.delete(0, tk.END)
        for var in self.genre_vars.values():
            var.set(False)
    
    def import_from_file(self):
        """Import songs from audio files"""
        file_types = [
            ("Audio Files", "*.mp3 *.wav *.flac *.m4a *.aac *.ogg"),
            ("MP3 Files", "*.mp3"),
            ("WAV Files", "*.wav"),
            ("FLAC Files", "*.flac"),
            ("All Files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select songs to import",
            filetypes=file_types,
            initialdir=os.path.expanduser("~/Music")
        )
        
        if not files:
            return
        
        # Create import window
        import_window = tk.Toplevel(self.root)
        import_window.title("Import Songs - Select Genres")
        import_window.geometry("600x500")
        import_window.configure(bg="#f0f0f0")
        
        # Create frame for imports
        canvas_frame = ttk.Frame(import_window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas with scrollbar
        canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Store import data
        import_data = {}
        
        for file_path in files:
            # Extract filename without extension
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # Try to extract song name and artist from filename (assuming "Artist - Song" format)
            if " - " in file_name:
                artist, song_name = file_name.rsplit(" - ", 1)
            else:
                artist = "Unknown"
                song_name = file_name
            
            # Create frame for this song
            song_frame = ttk.LabelFrame(scrollable_frame, text=f"📄 {song_name}", padding=10)
            song_frame.pack(fill=tk.X, pady=5)
            
            # Artist entry
            ttk.Label(song_frame, text="Artist:").grid(row=0, column=0, sticky=tk.W, pady=5)
            artist_entry = ttk.Entry(song_frame, width=40)
            artist_entry.insert(0, artist)
            artist_entry.grid(row=0, column=1, pady=5, padx=5)
            
            # Genre checkboxes
            ttk.Label(song_frame, text="Select Genres:").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
            
            genre_vars = {}
            for i, genre in enumerate(self.genres):
                var = tk.BooleanVar()
                genre_vars[genre] = var
                checkbox = ttk.Checkbutton(song_frame, text=genre, variable=var)
                checkbox.grid(row=2+i//3, column=i%3, sticky=tk.W, padx=5)
            
            import_data[file_path] = {
                "song_name": song_name,
                "artist_entry": artist_entry,
                "genre_vars": genre_vars
            }
        
        # Bottom buttons
        button_frame = ttk.Frame(import_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def save_imports():
            """Save all imported songs"""
            saved_count = 0
            for file_path, data in import_data.items():
                song_name = data["song_name"]
                artist = data["artist_entry"].get().strip()
                selected_genres = [genre for genre, var in data["genre_vars"].items() if var.get()]
                
                if not artist:
                    messagebox.showwarning("Missing Info", f"Please enter artist for '{song_name}'")
                    return
                
                if not selected_genres:
                    messagebox.showwarning("Missing Info", f"Please select at least one genre for '{song_name}'")
                    return
                
                # Add to database
                song_key = f"{song_name} - {artist}"
                self.songs[song_key] = {
                    "name": song_name,
                    "artist": artist,
                    "genres": selected_genres,
                    "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "file_path": file_path
                }
                saved_count += 1
            
            self.save_songs()
            messagebox.showinfo("Success", f"Successfully imported {saved_count} song(s)!")
            self.refresh_display()
            import_window.destroy()
        
        ttk.Button(button_frame, text="Save All Songs", command=save_imports).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=import_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def refresh_display(self):
        """Refresh the song display list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add songs
        for song_key, song_data in sorted(self.songs.items()):
            genres_str = ", ".join(song_data["genres"])
            self.tree.insert("", tk.END, values=(song_data["name"], song_data["artist"], genres_str))
        
        # Update status
        total_songs = len(self.songs)
        self.status_var.set(f"Ready | Total Songs: {total_songs}")
    
    def delete_song(self):
        """Delete selected song"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a song to delete!")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        song_name = values[0]
        artist = values[1]
        song_key = f"{song_name} - {artist}"
        
        if messagebox.askyesno("Confirm", f"Delete '{song_name}' by {artist}?"):
            del self.songs[song_key]
            self.save_songs()
            self.refresh_display()
            messagebox.showinfo("Success", "Song deleted!")
    
    def edit_song(self):
        """Edit selected song"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a song to edit!")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        song_name = values[0]
        artist = values[1]
        song_key = f"{song_name} - {artist}"
        
        song_data = self.songs[song_key]
        
        # Populate fields
        self.song_name_entry.delete(0, tk.END)
        self.song_name_entry.insert(0, song_data["name"])
        
        self.artist_entry.delete(0, tk.END)
        self.artist_entry.insert(0, song_data["artist"])
        
        # Reset all checkboxes
        for var in self.genre_vars.values():
            var.set(False)
        
        # Check selected genres
        for genre in song_data["genres"]:
            if genre in self.genre_vars:
                self.genre_vars[genre].set(True)
        
        messagebox.showinfo("Edit Mode", "Modify the song details and click 'Add/Update Song' to save changes.")
    
    def export_csv(self):
        """Export songs to CSV file"""
        if not self.songs:
            messagebox.showwarning("Empty Library", "No songs to export!")
            return
        
        csv_file = "songs_export.csv"
        try:
            with open(csv_file, 'w', encoding='utf-8') as f:
                f.write("Song Name,Artist,Genres,Added Date\n")
                for song_data in self.songs.values():
                    genres_str = "; ".join(song_data["genres"])
                    f.write(f"{song_data['name']},{song_data['artist']},\"{genres_str}\",{song_data['added_date']}\n")
            
            messagebox.showinfo("Export Success", f"Songs exported to {csv_file}!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicGenreBot(root)
    root.mainloop()
