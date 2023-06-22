import os
import re

def sanitize_playlist_name(name):
    return re.sub(r'[^a-zA-Z0-9 ]', '', name)

def create_album_playlists(path, playlist_dir):
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
                            song_path = os.path.join(album_path)
                            relative_path = os.path.relpath(song_path, playlist_dir).replace("..", "")
                            artist_playlist_file.write(f'file:///media/riley/Expansion{relative_path}\n')
                            break

            for album_name in sorted(albums):  # Sort the albums
                album_path = os.path.join(path, artist_name, album_name)
                album_playlist_name = sanitize_playlist_name(album_name)
                album_playlist_path = os.path.join(playlist_dir, f'{album_playlist_name}.m3u')
                album_playlist_path = get_unique_playlist_name(album_playlist_path, playlist_paths)
                playlist_paths.append(album_playlist_path)
                with open(album_playlist_path, 'w') as album_playlist_file:
                    # Write the album name as the first line in the playlist
                    album_playlist_file.write(f'# Album: {album_name.lower()}\n\n')

                    for root, dirs, files in os.walk(album_path):
                        for file in files:
                            if file.lower().endswith('.aif') or file.lower().endswith('.aiff'):
                                if file.startswith("._"):
                                    continue
                                song_path = os.path.join(album_path, file)
                                song_path2 = os.path.join(album_path)
                                relative_path = os.path.relpath(song_path, playlist_dir).replace("..", "")
                                relative_path2 = os.path.relpath(song_path2, playlist_dir).replace("..", "")
                                album_playlist_file.write(f'file:///media/riley/Expansion{relative_path2}\n')

def create_song_playlists(path, playlist_dir):
    existing_paths = []
    for root, dirs, files in os.walk(playlist_dir):
        for file in files:
            existing_paths.append(os.path.join(root, file))

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.aif') or file.lower().endswith('.aiff'):
                if file.startswith("._"):
                    continue
                song_path = os.path.join(root, file)
                relative_path = os.path.relpath(song_path, playlist_dir).replace("..", "")
                song_name = os.path.splitext(file)[0]
                sanitized_song_name = re.sub(r'^\d+[-\s]?\d*\s*', '', song_name)
                playlist_name = f"{sanitize_playlist_name(sanitized_song_name).lower()}.m3u"
                playlist_path = os.path.join(playlist_dir, playlist_name)
                playlist_path = get_unique_playlist_name(playlist_path, existing_paths)
                existing_paths.append(playlist_path)
                album_path = os.path.dirname(song_path)
                album_files = sorted([f for f in os.listdir(album_path) if f.lower().endswith('.aif') or f.lower().endswith('.aiff') and not f.startswith("._")])
                album_songs = []
                current_song_index = None

                for index, album_file in enumerate(album_files):
                    album_song_path = os.path.join(album_path, album_file)
                    album_relative_path = os.path.relpath(album_song_path, playlist_dir).replace("..", "")
                    if album_relative_path == relative_path:
                        current_song_index = index
                        album_songs.append(album_relative_path)
                    elif current_song_index is not None and index > current_song_index:
                        album_songs.append(album_relative_path)

                with open(playlist_path, 'a') as playlist_file:  # Append mode to add remaining songs
                    for song_relative_path in album_songs:
                        playlist_file.write(f'file:///media/riley/Expansion{song_relative_path}\n')


def get_unique_playlist_name(playlist_path, existing_paths):
    base_dir = os.path.dirname(playlist_path)
    base_name = os.path.splitext(os.path.basename(playlist_path))[0]
    counter = 1
    new_path = playlist_path
    while new_path in existing_paths:
        new_name = f'{base_name} {counter}'
        new_path = os.path.join(base_dir, f'{new_name.lower()}.m3u')
        counter += 1
    return new_path

# Set the path to the main folder and the playlist directory

path = '/media/riley/Expansion/Media/Music'
playlist_dir = '/media/riley/Expansion/xxxfinallowerrr999'
# Create the playlist directory if it doesn't exist
if not os.path.exists(playlist_dir):
    os.makedirs(playlist_dir)

create_album_playlists(path, playlist_dir)
create_song_playlists(path, playlist_dir)