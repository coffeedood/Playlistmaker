import os
import re

def create_artist_playlists(path, playlist_dir):
    artists = {}
    playlist_paths = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.aif') or file.lower().endswith('.aiff'):
                artist_name = os.path.basename(os.path.dirname(root))
                album_name = os.path.basename(root)
                if artist_name not in artists:
                    artists[artist_name] = set()
                artists[artist_name].add(album_name)

    for artist_name, albums in artists.items():
        artist_playlist_path = os.path.join(playlist_dir, f'{artist_name.lower()}.m3u')
        artist_playlist_path = get_unique_playlist_name(artist_playlist_path, playlist_paths)
        playlist_paths.append(artist_playlist_path)
        with open(artist_playlist_path, 'w') as artist_playlist_file:
            for album_name in sorted(albums):
                album_path = os.path.join(path, artist_name, album_name)
                for root, dirs, files in os.walk(album_path):
                    for file in files:
                        if file.lower().endswith('.aif') or file.lower().endswith('.aiff'):
                            song_path = os.path.join(album_path, file)
                            relative_path = os.path.relpath(song_path, playlist_dir).replace("..", "")
                            artist_playlist_file.write(f'file:///media/riley/Expansion{relative_path}\n')

def create_album_playlists(path, playlist_dir):
    albums = {}
    playlist_paths = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.aif') or file.lower().endswith('.aiff'):
                album_name = os.path.basename(root)
                artist_name = os.path.basename(os.path.dirname(root))
                if artist_name not in albums:
                    albums[artist_name] = {}
                if album_name not in albums[artist_name]:
                    albums[artist_name][album_name] = set()
                albums[artist_name][album_name].add(file)

    for artist_name, artist_albums in albums.items():
        for album_name, songs in artist_albums.items():
            album_playlist_path = os.path.join(playlist_dir, f'{album_name.lower()}.m3u')
            album_playlist_path = get_unique_playlist_name(album_playlist_path, playlist_paths)
            playlist_paths.append(album_playlist_path)
            with open(album_playlist_path, 'w') as album_playlist_file:
                for song in sorted(songs):
                    song_path = os.path.join(path, artist_name, album_name, song)
                    relative_path = os.path.relpath(song_path, playlist_dir).replace("..", "")
                    album_playlist_file.write(f'file:///media/riley/Expansion{relative_path}\n')

# ...

# ...

def create_song_playlists(path, playlist_dir):
    existing_paths = []
    for root, dirs, files in os.walk(playlist_dir):
        for file in files:
            existing_paths.append(os.path.join(root, file))

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.aif') or file.lower().endswith('.aiff'):
                song_path = os.path.join(root, file)
                relative_path = os.path.relpath(song_path, playlist_dir).replace("..", "")
                song_name = os.path.splitext(file)[0].lower()
                song_name = re.sub(r"^\d+\s+", '', song_name)  # Remove track numbers and leading space
                song_name = re.sub(r"[^\w\s'\-]", '', song_name)  # Remove invalid characters from the song name
                song_playlist_path = os.path.join(playlist_dir, f'{song_name}.m3u')
                song_playlist_path = get_unique_playlist_name(song_playlist_path, existing_paths)
                existing_paths.append(song_playlist_path)
                with open(song_playlist_path, 'w') as song_playlist_file:
                    song_playlist_file.write(f'file:///media/riley/Expansion{relative_path}\n')

# ...



# ...


def get_unique_playlist_name(playlist_path, existing_paths):
    base_dir = os.path.dirname(playlist_path)
    base_name = os.path.splitext(os.path.basename(playlist_path))[0]
    counter = 1
    new_path = playlist_path
    while new_path in existing_paths:
        new_name = f'{base_name} {counter}'  # Use space and counter instead of underscore
        new_path = os.path.join(base_dir, f'{new_name}.m3u')
        counter += 1
    return new_path

# Set the path to the main folder and the playlist directory
path = '/media/riley/Expansion/Media/Music'
playlist_dir = '/media/riley/Expansion/1234321'

# Create the playlist directory if it doesn't exist
if not os.path.exists(playlist_dir):
    os.makedirs(playlist_dir)

# Create playlists for artists, albums, and songs
create_artist_playlists(path, playlist_dir)
create_album_playlists(path, playlist_dir)
create_song_playlists(path, playlist_dir)
